from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('procesos/<str:red>', views.Procesos, name='procesos'),
    path('solicitud', views.Solicitud, name='solicitud'),
    path('list', views.list_sol, name='lista'),
    path('status/<str:red>/<str:producto>/<int:cantidad>', views.estatus, name='estatus'),
    path('pEjecucion/<str:transicion>/<str:produccion>', views.ProcesosEjecucion, name='pEjecucion'),
    path('sProduccion', views.SeleccionProduccion, name='sProduccion'),
    path('produccion/<str:producto>', views.Produccion, name='produccion'),
]
