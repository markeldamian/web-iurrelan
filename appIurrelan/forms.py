from django import forms
from django_recaptcha.fields import ReCaptchaField
from django.utils.translation import gettext_lazy as _

class DenunciaForm(forms.Form):
    contacto = forms.CharField(
        label=_('Datos de contacto (Opcional)'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan Pérez - juan@email.com o Tel: 123456789'})
    )
    asunto = forms.CharField(
        label=_('Asunto de la denuncia'),
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Resumen breve de la comunicación...')})
    )
    hechos = forms.CharField(
        label=_('Descripción de los hechos'),
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': _('Describa de la forma más detallada posible los hechos...')})
    )
    captcha = ReCaptchaField(
        label=_('Verificación de seguridad')
    )
    privacidad = forms.BooleanField(
        label=_('He leído y acepto la Política de Privacidad y comprendo el funcionamiento del Canal Ético.'),
        required=True
    )
class ContactoForm(forms.Form):
    nombre = forms.CharField(required=True, label=_("Nombre Completo"), widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': _('Tu nombre')}))
    email = forms.EmailField(required=True, label=_("Correo Electrónico"), widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ejemplo@correo.com'}))
    telefono = forms.CharField(required=False, label=_("Teléfono (Opcional)"), widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+34 ...'}))
    mensaje = forms.CharField(required=True, label=_("Mensaje"), widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'placeholder': _('¿En qué podemos ayudarte?')}))
    privacidad = forms.BooleanField(required=True, label=_("He leído y acepto la Política de Privacidad"))
    captcha = ReCaptchaField(label=_("Seguridad"))


# === NUEVO FORMULARIO DE EMPLEO ===
class EmpleoForm(forms.Form):
    nombre_candidato = forms.CharField(
        label=_("Nombre y Apellidos"), 
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': _('Tu nombre completo')})
    )
    email_candidato = forms.EmailField(
        label=_("Correo Electrónico"),
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ejemplo@correo.com'})
    )
    telefono_candidato = forms.CharField(
        label=_("Teléfono"), 
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+34 ...'})
    )
    experiencia = forms.CharField(
        label=_("Experiencia / Presentación"), 
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': _('Háblanos de tu experiencia laboral...')})
    )
    curriculum = forms.FileField(
        label=_("Adjuntar Currículum (PDF) - Opcional"), 
        required=False,  # Ponlo en True si quieres que sea obligatorio
        widget=forms.FileInput(attrs={'accept': 'application/pdf', 'class': 'form-input'})
    )
    privacidad_empleo = forms.BooleanField(
        label=_("He leído y acepto la Política de Privacidad"), 
        required=True
    )

    def clean_curriculum(self):
        file = self.cleaned_data.get('curriculum')
        if file:
            if not file.name.lower().endswith('.pdf'):
                raise forms.ValidationError(_("El archivo debe ser un documento PDF."))
            if file.size > 5 * 1024 * 1024:  # Limite 5MB
                raise forms.ValidationError(_("El archivo es demasiado grande (máximo 5MB)."))
        return file