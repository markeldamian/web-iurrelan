from django import forms
from django_recaptcha.fields import ReCaptchaField
from django.utils.translation import gettext_lazy as _

class DenunciaForm(forms.Form):
    # El campo de nombre/email es OPCIONAL para garantizar el anonimato
    contacto = forms.CharField(
        required=False, 
        label=_(u"Datos de contacto (Opcional)"),
        widget=forms.TextInput(attrs={
            'placeholder': 'Dejar en blanco para denuncia anónima',
            'class': 'form-input'
        })
    )
    asunto = forms.CharField(
        required=True,
        label="Asunto de la denuncia",
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: Incumplimiento de normativa de seguridad...',
            'class': 'form-input'
        })
    )
    mensaje = forms.CharField(
        required=True,
        label=_("Descripción de los hechos"),
        widget=forms.Textarea(attrs={
            'placeholder': 'Describa los hechos con el mayor detalle posible...',
            'class': 'form-textarea',
            'rows': 5
        })
    )
    
    # --- AÑADIR EL CAPTCHA ---
    captcha = ReCaptchaField(label=_("Verificación de seguridad")) 
    privacidad = forms.BooleanField(
        required=True,
        label=_("He leído y acepto la Política de Privacidad y comprendo el funcionamiento del Canal Ético.")
    )
    privacidad = forms.BooleanField(
        required=True,
        label=_("He leído y acepto la Política de Privacidad y comprendo el funcionamiento del Canal Ético.")
    )


class ContactoForm(forms.Form):
    nombre = forms.CharField(
        required=True,
        label=_("Nombre Completo"),
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tu nombre'})
    )
    email = forms.EmailField(
        required=True,
        label=_("Correo Electrónico"),
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ejemplo@correo.com'})
    )
    telefono = forms.CharField(
        required=False,
        label=_("Teléfono (Opcional)"),
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+34 ...'})
    )
    mensaje = forms.CharField(
        required=True,
        label=_("Mensaje"),
        widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'placeholder': '¿En qué podemos ayudarte?'})
    )
    privacidad = forms.BooleanField(
        required=True,
        label=_("He leído y acepto la Política de Privacidad")
    )
    captcha = ReCaptchaField(label="Seguridad")