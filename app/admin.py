from django.contrib import admin
from .models import Lugares, Transiciones, ArcosEntradas, ArcosSalidas, TipoLugar, RedDePetri
# Register your models here.

admin.site.register(Lugares)
admin.site.register(Transiciones)
admin.site.register(ArcosEntradas)
admin.site.register(ArcosSalidas)
admin.site.register(RedDePetri)
admin.site.register(TipoLugar)
