from django.contrib import admin
from .models import Maquina

@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'orden')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'descripcion')