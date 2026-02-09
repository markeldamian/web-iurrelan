from django.db import models
from django.utils.translation import gettext_lazy as _  # <--- 1. IMPORTANTE: Añadir esta línea

class CategoriaMaquina(models.TextChoices):
    # 2. Envolver el segundo texto de cada línea con _( ... )
    CORTE = 'CORTE', _('Corte Láser')
    SOLDADURA = 'SOLDADURA', _('Soldadura')
    MECANIZADO = 'MECANIZADO', _('Mecanizado')
    OTROS = 'OTROS', _('Auxiliares') # He puesto 'Auxiliares' para coincidir con tu traducción

class Maquina(models.Model):
    # Opcional: También puedes traducir los nombres de los campos para el panel de administración
    nombre = models.CharField(_('Nombre'), max_length=100)
    descripcion = models.TextField(_('Descripción'))
    
    categoria = models.CharField(
        _('Categoría'),
        max_length=20,
        choices=CategoriaMaquina.choices,
        default=CategoriaMaquina.CORTE
    )
    
    imagen = models.ImageField(_('Imagen'), upload_to='maquinaria/', blank=True, null=True)
    specs = models.CharField(_('Especificaciones'), max_length=200, help_text=_("Ej: 6000W, 5 Ejes, etc."), blank=True)
    orden = models.IntegerField(_('Orden'), default=0, help_text=_("Orden de aparición"))

    class Meta:
        ordering = ['orden']
        verbose_name = _("Máquina")
        verbose_name_plural = _("Maquinaria")

    def __str__(self):
        return self.nombre