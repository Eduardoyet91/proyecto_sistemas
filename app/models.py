from django.db import models

class TipoLugar(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

# Create your models here.
class Lugares(models.Model):
    nombre = models.CharField(max_length=100)
    tokens = models.PositiveIntegerField(default=0)
    tiempo = models.PositiveIntegerField(default=0)
    tipo = models.ForeignKey(TipoLugar, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class Transiciones(models.Model):
    nombre = models.CharField(max_length=100)
    habilitada = models.BooleanField(default = False)
    def __str__(self):
        return self.nombre

class ArcosEntradas(models.Model):
    origen = models.ForeignKey(Lugares, on_delete=models.CASCADE)
    destino = models.ForeignKey(Transiciones, on_delete=models.CASCADE)
    peso = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.origen} -> {self.destino}"

class ArcosSalidas(models.Model):
    origen = models.ForeignKey(Transiciones, on_delete=models.CASCADE)
    destino = models.ForeignKey(Lugares, on_delete=models.CASCADE)
    peso = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.origen}  ->  {self.destino}"

class RedDePetri(models.Model):
    nombre = models.CharField(max_length=100)
    lugares = models.ManyToManyField(Lugares)
    transiciones = models.ManyToManyField(Transiciones)
    arcosentradas = models.ManyToManyField(ArcosEntradas)
    arcossalidas = models.ManyToManyField(ArcosSalidas)

    def __str__(self):
        return self.nombre
    


