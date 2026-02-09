from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import DenunciaForm, ContactoForm 
from .models import Maquina # Asegúrate de importar el modelo


# ... tus otras vistas (home_view, etc) ...
def empresa_view(request):
    return render(request, 'empresa.html')

def cortedos(request):
    return render(request, 'corte2.html')
def acabado(request):
    return render(request, 'acabado.html')
def soldadura(request):
    return render(request, 'soldadura.html')

def mecanizado(request):
    return render(request, 'mecanizado.html')

def corte(request):
    return render(request, 'corte.html')

def granallado(request):
    return render(request, 'granallado.html')
def rebarbado(request):
    return render(request, 'rebarbado.html')
def servicios(request):
    return render(request, 'servicios.html')


def maquinaria(request):
    maquinas = Maquina.objects.all()
    # Obtenemos las categorías únicas para los botones de filtro
    categorias = Maquina.objects.values_list('categoria', flat=True).distinct()
    return render(request, 'maquinaria.html', {'maquinas': maquinas, 'categorias': set(categorias)})

def canal_etico_view(request):
    if request.method == 'POST':
        form = DenunciaForm(request.POST)
        if form.is_valid():
            # Extraer datos
            asunto = form.cleaned_data['asunto']
            mensaje_usuario = form.cleaned_data['mensaje']
            contacto = form.cleaned_data['contacto'] or "ANÓNIMO"
            
            # Crear el cuerpo del correo
            cuerpo_email = f"""
            NUEVA DENUNCIA RECIBIDA DESDE LA WEB (CANAL ÉTICO)
            ----------------------------------------------------
            ASUNTO: {asunto}
            
            IDENTIDAD DEL DENUNCIANTE: {contacto}
            
            DESCRIPCIÓN DE LOS HECHOS:
            {mensaje_usuario}
            
            ----------------------------------------------------
            Este es un mensaje automático del sistema de cumplimiento normativo.
            Se debe acusar recibo al denunciante en un plazo de 7 días (si facilitó contacto).
            """
            
            # Enviar el correo
            try:
                send_mail(
                    subject=f'CANAL ÉTICO: {asunto}',
                    message=cuerpo_email,
                    from_email='pruebamprog@gmail.com', # Remitente
                    recipient_list=['pruebamprog@gmail.com'], # Destinatario
                    fail_silently=False,
                )
                messages.success(request, 'Su denuncia ha sido enviada correctamente. Gracias por su colaboración.')
                return redirect('home') # O redirigir a una página de "gracias"
            except Exception as e:
                messages.error(request, 'Error al enviar la denuncia. Por favor, inténtelo más tarde.')
                
    else:
        form = DenunciaForm()

    return render(request, 'legal/canal_etico.html', {'form': form})
def ejemplo_view(request):
     return render(request, 'ejemplo.html')
# Create your views here.

def home_view(request):
    return render(request, 'home.html')



def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Extraer datos
            nombre = form.cleaned_data['nombre']
            email_cliente = form.cleaned_data['email']
            telefono = form.cleaned_data.get('telefono', 'No indicado')
            mensaje = form.cleaned_data['mensaje']
            
            cuerpo_email = f"""
            NUEVO MENSAJE DE CONTACTO WEB
            -----------------------------
            Nombre: {nombre}
            Email: {email_cliente}
            Teléfono: {telefono}
            
            Mensaje:
            {mensaje}
            """
            
            try:
                send_mail(
                    subject=f'CONTACTO WEB: Mensaje de {nombre}',
                    message=cuerpo_email,
                    from_email='pruebamprog@gmail.com',
                    recipient_list=['pruebamprog@gmail.com'], # Tu email
                    fail_silently=False,
                )
                messages.success(request, 'Mensaje enviado correctamente. Nos pondremos en contacto contigo pronto.')
                return redirect('contacto')
            except Exception as e:
                messages.error(request, 'Error al enviar el mensaje. Inténtalo de nuevo.')
        else:
            messages.error(request, 'No se ha podido enviar. Por favor, revisa los campos en rojo y el Captcha.')
    else:
        form = ContactoForm()

    return render(request, 'contacto.html', {'form': form})