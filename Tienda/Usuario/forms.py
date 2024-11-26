from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.safestring import mark_safe

from Tienda.models import Datos

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('El correo electrónico ya está en uso.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso.')
        return username
    
class EditDatosUserForm(forms.ModelForm):
    def as_custom(self):
        output = []
        for field in self.visible_fields():
            output.append(f'<label>{field} <span>{field.label}</span></label>')
        return mark_safe('\n'.join(output))
    class Meta:
        model = Datos
        fields = ['direccion', 'metodo_de_pago']
        widgets = {
            'direccion': forms.TextInput(attrs={
                'class': 'input'
            }),
            'metodo_de_pago': forms.Select(attrs={
                'class': 'input',
                'requerided': False
            }),
        }

class EditPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            field.required = False  # Hacer que los campos no sean obligatorios

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if old_password or new_password1 or new_password2:
            if not old_password:
                self.add_error('old_password', 'Este campo es obligatorio.')
            if not new_password1:
                self.add_error('new_password1', 'Este campo es obligatorio.')
            if not new_password2:
                self.add_error('new_password2', 'Este campo es obligatorio.')

        return cleaned_data
