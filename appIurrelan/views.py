import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.urls import reverse
from .forms import DenunciaForm, ContactoForm, EmpleoForm 
from .models import Maquina


# ... tus otras vistas (home_view, etc) ...
def empresa_view(request):
    return render(request, 'empresa.html')

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
            contacto = form.cleaned_data.get('contacto', 'Anónimo')
            asunto = form.cleaned_data['asunto'] # <-- Recogemos el asunto
            hechos = form.cleaned_data['hechos']
            
            # Si el usuario lo deja en blanco, lo marcamos como Anónimo explícitamente
            if not contacto.strip():
                contacto = "Anónimo"

            # Construimos el cuerpo del correo con los datos reales
            cuerpo_mensaje = f"""
NUEVA COMUNICACIÓN - CANAL ÉTICO
--------------------------------

ASUNTO: {asunto}

DATOS DE CONTACTO:
{contacto}

DESCRIPCIÓN DE LOS HECHOS:
{hechos}

--------------------------------
Este mensaje ha sido enviado desde el formulario seguro de la página web de Iurrelan.
"""

            try:
                # Enviamos el correo usando send_mail
                email= EmailMessage(
                    subject=f'DENUNCIA: {asunto}', # <-- Ponemos el asunto del usuario en el asunto del mail
                    body=cuerpo_mensaje,
                    from_email='iurrelanweb@gmail.com', # Remitente del sistema
                    to=['canaldenuncias@aitabogados.com'], # Destinatario final
                )
                email.send(fail_silently=False)

                # Mensaje de éxito para el usuario
                messages.success(request, 'Su comunicación ha sido enviada de forma segura y confidencial.')
                return redirect('canal_etico')
                
            except Exception as e:
                # Si falla el correo, mostramos el error exacto en pantalla para depurar
                messages.error(request, f'Hubo un error del servidor al enviar la comunicación: {e}')
        else:
            messages.error(request, 'Por favor, corrija los errores del formulario antes de enviar.')
    else:
        form = DenunciaForm()
        
    return render(request, 'legal/canal_etico.html', {'form': form})
def home_view(request):
    return render(request, 'home.html')


def contacto_view(request):
    form_contacto = ContactoForm()
    form_empleo = EmpleoForm()

    if request.method == 'POST':
        # ====================================================
        # 1. PROCESAR FORMULARIO DE CONTACTO GENERAL
        # ====================================================
        if 'btn_contacto' in request.POST:
            form_contacto = ContactoForm(request.POST)
            if form_contacto.is_valid():
                nombre = form_contacto.cleaned_data['nombre']
                email_cliente = form_contacto.cleaned_data['email']
                telefono = form_contacto.cleaned_data.get('telefono', 'No indicado')
                mensaje = form_contacto.cleaned_data['mensaje']
                
                cuerpo_email = f"NUEVO MENSAJE DE CONTACTO WEB\n-----------------------------\nNombre: {nombre}\nEmail: {email_cliente}\nTeléfono: {telefono}\n\nMensaje:\n{mensaje}"
                
                try:
                    email = EmailMessage(
                        subject=f'CONTACTO WEB: Mensaje de {nombre}',
                        body=cuerpo_email,
                        from_email='iurrelanweb@gmail.com', # Cambia a tu remitente
                        to=['administracion@iurrelan.com'],       # Cambia al correo de la empresa
                        reply_to=[email_cliente],
                    )
                    email.send(fail_silently=False)
                    messages.success(request, 'Mensaje enviado correctamente. Nos pondremos en contacto contigo pronto.')
                    return redirect('contacto') # Asegúrate de que el nombre de la url es 'contacto'
                except Exception as e:
                    messages.error(request, f'Error al enviar el mensaje de contacto: {e}')
            else:
                messages.error(request, 'Error en el formulario de contacto. Revisa los campos marcados.')

        # ====================================================
        # 2. PROCESAR FORMULARIO DE EMPLEO
        # ====================================================
        elif 'btn_empleo' in request.POST:
            form_empleo = EmpleoForm(request.POST, request.FILES)
            if form_empleo.is_valid():
                nombre = form_empleo.cleaned_data['nombre_candidato']
                email_usr = form_empleo.cleaned_data['email_candidato']
                telefono = form_empleo.cleaned_data['telefono_candidato']
                experiencia = form_empleo.cleaned_data['experiencia']
                archivo_cv = request.FILES.get('curriculum')

                cuerpo_email = f"""
NUEVO CANDIDATO - TRABAJA CON NOSOTROS
--------------------------------------
Nombre: {nombre}
Email: {email_usr}
Teléfono: {telefono}

Experiencia / Presentación:
{experiencia}
"""
                try:
                    email = EmailMessage(
                        subject=f"CV RECIBIDO: {nombre}",
                        body=cuerpo_email,
                        from_email='iurrelanweb@gmail.com', # Cambia a tu remitente
                        to=['administracion@iurrelan.com'],       # Cambia al correo de rrhh/empresa
                        reply_to=[email_usr],
                    )
                    
                    # Adjuntar archivo de forma segura usando un archivo temporal
                    if archivo_cv:
                        temp_file_path = os.path.join(settings.BASE_DIR, archivo_cv.name)
                        with open(temp_file_path, 'wb+') as destination:
                            for chunk in archivo_cv.chunks():
                                destination.write(chunk)
                        
                        email.attach_file(temp_file_path)
                        email.send(fail_silently=False)
                        os.remove(temp_file_path)
                    else:
                        email.send(fail_silently=False)

                    messages.success(request, 'Tus datos han sido enviados con éxito. ¡Gracias por tu interés en trabajar con nosotros!')
                    # Redirige anclado a la sección de empleo
                    url = reverse('contacto') + '#trabaja-con-nosotros'
                    return redirect(url)
                    
                except Exception as e:
                    print(f"ERROR AL ENVIAR CORREO DE EMPLEO: {e}")
                    # Limpieza por si falla
                    if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                    messages.error(request, f'Hubo un error del servidor al enviar tus datos: {e}')
            else:
                messages.error(request, 'Error en el formulario de empleo. Revisa los campos.')

    context = {
        'form': form_contacto,
        'form_empleo': form_empleo,
    }
    return render(request, 'contacto.html', context)