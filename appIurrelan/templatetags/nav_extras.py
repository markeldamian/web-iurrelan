from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag(takes_context=True)
def is_active(context, url_names):
    """
    Devuelve 'active' si la URL actual coincide con alguno de los nombres pasados (separados por espacio).
    Uso: {% is_active 'home' %} o {% is_active 'corte soldadura mecanizado' %}
    """
    request = context['request']
    try:
        current_url_name = resolve(request.path_info).url_name
        if current_url_name in url_names.split():
            return 'active'
    except:
        pass
    return ''