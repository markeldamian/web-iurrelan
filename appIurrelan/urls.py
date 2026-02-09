from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView 

urlpatterns = [
    path('ej/', views.ejemplo_view, name='ejemplo'),
    path('', views.home_view, name='home'),

    path('aviso-legal/', TemplateView.as_view(template_name="legal/aviso_legal.html"), name='aviso_legal'),
    path('privacidad/', TemplateView.as_view(template_name="legal/privacidad.html"), name='privacidad'),
    path('cookies/', TemplateView.as_view(template_name="legal/cookies.html"), name='cookies'),
    path('canal-etico/', views.canal_etico_view, name='canal_etico'),
    path('empresa/', views.empresa_view, name='empresa'),
    path('contacto/', views.contacto_view, name='contacto'),
    path('servicios/', views.servicios, name='servicios'),
    path('servicios/corte2/', views.cortedos, name='corte2'),
    path('servicios/corte/', views.corte, name='corte'),
    path('servicios/acabado/', views.acabado, name='acabado'),
    path('servicios/soldadura/', views.soldadura, name='soldadura'),
    path('servicios/mecanizado/', views.mecanizado, name='mecanizado'),
    path('servicios/rebarbado/', views.rebarbado, name='rebarbado'),
    path('servicios/granallado/', views.granallado, name='granallado'),
    path('maquinaria/', views.maquinaria, name='maquinaria'),
]