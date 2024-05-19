from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import RedDePetri, ArcosEntradas, ArcosSalidas, Transiciones, Lugares
# Create your views here.

def index(request):
    return render(request, 'pages/index.html',
    {
    })

def Procesos(red):
    procesos = RedDePetri.objects.filter(id=red)
# Mostrar las transiciones disponibles
    arcosEntradas = ArcosEntradas.objects.all()
    transicion = Transiciones.objects.all()
    numPlazas = 0
    plazasActivas = 0
    for t in transicion: # Revisar todas las transiciones
        arcos = ArcosEntradas.objects.filter(destino=t.id)  # Revisar solo los arcos d la transicion
        
        for p in arcos: # verificar si estas plazas esta listas
            numPlazas += 1 # numero de plazas
            plaza = Lugares.objects.get(id=p.origen.id) 
            if p.peso <= plaza.tokens:
                plazasActivas += 1 # numero de plazas activas
        if numPlazas == plazasActivas:
            t.habilitada = True
            t.save()
        else:
            t.habilitada = False
            t.save()
        numPlazas = 0
        plazasActivas = 0
# Salida en pantalla
   





def Solicitud(request):
    # Valores para la lista desplegable
    
    opciones = RedDePetri.objects.exclude(nombre="Planificador").values_list('nombre', flat=True)
    red = RedDePetri.objects.filter(nombre="Planificador")
    planificador = red[0]

    eliminar(planificador.id)

    # Si el formulario ha sido enviado
    if request.method == 'POST':
        # Obtener los datos del formulario
        valor_lista = request.POST.get('producto')
        valor_input = request.POST.get('campo_input')
        transicion_id = request.POST.get('transicion_id')

     
        
        return redirect(reverse('estatus', args=(planificador.id,valor_lista, valor_input)))

    return render(request, 'pages/solicitud.html', {'opciones': opciones, 'red':planificador})


def list_sol(request):
    return render(request, 'pages/list_solicitudes.html',
    {
    })

def estatus(request,red,producto,cantidad): 
    lugares = Lugares.objects.all()
    Modelo = RedDePetri.objects.filter(nombre=producto)
    modelos = RedDePetri.objects.exclude(nombre="Planificador").values_list('nombre', flat=True)
    print(Modelo[0].nombre)
    lugares_p = Modelo[0].lugares.all()
    lugares_insumo = Modelo[0].lugares.filter(tipo=3)
    lugares_unidad = Modelo[0].lugares.filter(tipo=4)
    red_petri = RedDePetri.objects.get(id=red)

    # Filtra las transiciones relacionadas con esa red de Petri
    transiciones_habilitadas = red_petri.transiciones.filter(habilitada=True)
    
    Equipos_plaza = red_petri.lugares.filter(nombre = "Analisis Equipos")
    Insumo_plaza = red_petri.lugares.filter(nombre = "Analisis Insumos")
    Recepcion_plaza = red_petri.lugares.filter(nombre = "Recepcion")
    Aceptacion_plaza = red_petri.lugares.filter(nombre = "Orden Aceptada")
    Enviar_orden = Modelo[0].lugares.filter(nombre = 'Orden')

    if Aceptacion_plaza[0].tokens == 1:
        Enviar_orden[0].tokens += cantidad
        print("Entre en acepacion")
        redirect(reverse('estatus', args=(red,producto,cantidad)))
        transiciones_produccion = Modelo[0].transiciones.filter(habilitada=True)
        print(transiciones_produccion[0].nombre)
        while len(transiciones_produccion) > 0:
            
            Ejecucion(transiciones_produccion[0].id,Modelo[0].id,producto,cantidad)
            transiciones_produccion = Modelo[0].transiciones.filter(habilitada=True)
 
    if Equipos_plaza[0].tokens == 1:
    # Comprobar la disponibilidad de los equipos
        disponible = True

        for l in lugares_unidad:
            if l.tokens != 0:
                disponible = False
                break
    
        if disponible:
        # if True:
            for t in transiciones_habilitadas:
                if t.nombre == "si equipo":
                    Ejecucion(t.id,red,producto,cantidad)
        else:
            for t in transiciones_habilitadas:
                if t.nombre == "no equipo":
                    Ejecucion(t.id,red,producto,cantidad)
    
    if Insumo_plaza[0].tokens == 1:
    # Comprobacion de los insumos para el modelo
        num_lugares = 0
        disponible = False
        aprobados = 0
    
        for l in lugares_insumo:
            num_lugares += 1
            arcos = ArcosEntradas.objects.filter(origen=l.id)
            for arco in arcos:
                if l.tokens >= (arco.peso * cantidad):
                    aprobados += 1 
        if num_lugares == aprobados: 
            disponible = True

    # Resultado
        if disponible:
            for t in transiciones_habilitadas:
                if t.nombre == "si insumo":
                    Ejecucion(t.id,red,producto,cantidad)
        else:
            for t in transiciones_habilitadas:
                if t.nombre == "no insumo":
                    Ejecucion(t.id,red,producto,cantidad)

    if Recepcion_plaza[0].tokens == 1:
          if Modelo:
                for t in transiciones_habilitadas:
                    if t.nombre == "analisis":
                        print(t.nombre)
                        Ejecucion(t.id,red,producto,cantidad)
          else:
                for t in transiciones_habilitadas:
                    if t.nombre == "sin Modelo":
                        Ejecucion(t.id,red,producto,cantidad)

    if len(transiciones_habilitadas) == 1:
        Ejecucion(transiciones_habilitadas[0].id,red,producto,cantidad)

    if len(transiciones_habilitadas) == 1:
        Ejecucion(transiciones_habilitadas[0].id,red,producto,cantidad)

    for t in transiciones_habilitadas:
                    if t.nombre == "Rechazo Insumo":
                        Ejecucion(t.id,red,producto,cantidad)
                    if t.nombre == "Rechazo Equipo":
                        Ejecucion(t.id,red,producto,cantidad)
    

    return render(request, 'pages/estatus.html',
    {
        'p':lugares,'l_p':lugares_p,'modelos':modelos
    })

def Ejecucion(transicion,red,producto,cantidad):   
    red_petri = RedDePetri.objects.filter(id=red)
    transicionActiva = Transiciones.objects.filter(id=transicion)

         # La transicion activada
    # Generar tokens de salida
    arcosSalidas = ArcosSalidas.objects.filter(origen=transicion)
    for p in arcosSalidas:
        plaza = Lugares.objects.get(id=p.destino.id)
        plaza.tokens += p.peso
        plaza.save()
    # Remover tokens consumidos
    arcosEntradas = ArcosEntradas.objects.filter(destino=transicion)
    for p in arcosEntradas:
        plaza = Lugares.objects.get(id=p.origen.id)
        plaza.tokens -= p.peso
        plaza.save()

# Mostrar las transiciones disponibles
    arcosEntradas = ArcosEntradas.objects.all()
    transicion = Transiciones.objects.all()
    numPlazas = 0
    plazasActivas = 0
    for t in transicion: # Revisar todas las transiciones
        arcos = ArcosEntradas.objects.filter(destino=t.id)  # Revisar solo los arcos d la transicion
        for p in arcos: # verificar si estas plazas esta listas
            numPlazas += 1 # numero de plazas
            plaza = Lugares.objects.get(id=p.origen.id) 
            if p.peso <= plaza.tokens:
                plazasActivas += 1 # numero de plazas activas
        if numPlazas == plazasActivas:
            t.habilitada = True
            t.save()
        else:
            t.habilitada = False
            t.save()
        numPlazas = 0
        plazasActivas = 0

        redirect(reverse('estatus', args=(red,producto,cantidad)))

   
def eliminar(red):
    red_petri = RedDePetri.objects.get(id=red)

    # Filtra las transiciones relacionadas con esa red de Petri
    lugares = red_petri.lugares.all()
    for l in lugares:
        if l.nombre != "Inicio":
            l.tokens = 0
            l.save()
            print(l.nombre)
            
        else:
            l.tokens = 1
            l.save()
    Procesos(red)



### Estado de la produccion  ### Solo copia en el otro views.py desde aqui abajo
## Elimina esta funcion def ProcesosEjecucion(request, transicion, produccion): de la parte de arriba
# para que te quedes con la nueva version

def SeleccionProduccion(request):
    opciones = RedDePetri.objects.exclude(nombre="Planificador").values_list('nombre', flat=True)
    return render(request, 'pages/sProduccion.html', {'opciones': opciones})

def Produccion(request,producto):
    produccion = RedDePetri.objects.get(nombre=producto)
    # Mostrar las transiciones disponibles
    arcosEntradas = ArcosEntradas.objects.all()
    transicion = Transiciones.objects.all()
    numPlazas = 0
    plazasActivas = 0
    for t in transicion: # Revisar todas las transiciones del proceso
        arcos = ArcosEntradas.objects.filter(destino=t.id)  # Revisar solo los arcos d la transicion
        
        for p in arcos: # verificar si estas plazas esta listas
            numPlazas += 1 # numero de plazas
            plaza = Lugares.objects.get(id=p.origen.id) 
            if p.peso <= plaza.tokens:
                plazasActivas += 1 # numero de plazas activas
        if numPlazas == plazasActivas:
            t.habilitada = True
            t.save()
        else:
            t.habilitada = False
            t.save()
        numPlazas = 0
        plazasActivas = 0
    return render(request, 'pages/produccion.html',
    {
        'produccion' : produccion,
    })

def ProcesosEjecucion(request, transicion, produccion):
    Modelo = RedDePetri.objects.filter(nombre=produccion)
    transicionActiva = Transiciones.objects.filter(id=transicion)

    # Generar tokens de salida
    arcosSalidas = ArcosSalidas.objects.filter(origen=transicion)
    for p in arcosSalidas:
        plaza = Lugares.objects.get(id=p.destino.id)
        plaza.tokens += p.peso
        plaza.save()
    # Remover tokens consumidos
    arcosEntradas = ArcosEntradas.objects.filter(destino=transicion)
    for p in arcosEntradas:
        plaza = Lugares.objects.get(id=p.origen.id)
        plaza.tokens -= p.peso
        plaza.save()

# Mostrar las transiciones disponibles
    arcosEntradas = ArcosEntradas.objects.all()
    transicion = Transiciones.objects.all()
    numPlazas = 0
    plazasActivas = 0
    for t in transicion: # Revisar todas las transiciones
        arcos = ArcosEntradas.objects.filter(destino=t.id)  # Revisar solo los arcos d la transicion
        for p in arcos: # verificar si estas plazas esta listas
            numPlazas += 1 # numero de plazas
            plaza = Lugares.objects.get(id=p.origen.id) 
            if p.peso <= plaza.tokens:
                plazasActivas += 1 # numero de plazas activas
        if numPlazas == plazasActivas:
            t.habilitada = True
            t.save()
        else:
            t.habilitada = False
            t.save()
        numPlazas = 0
        plazasActivas = 0
# Salida en pantalla  
    return render(request, 'pages/procesosEjecucion.html',
    {
        'transicion' : transicionActiva,
        'produccion' : Modelo[0],
    })
