from django import forms

from Tienda.models import Factura
from django.contrib.auth.models import User

class FormFactura(forms.Form):
    
    def __init__(self, *args, **kwargs):
        # Coge el atributo user entre los kwargs y lo borrar para eliminar error al pasar parametro a super.__init__()
        user:User = None
        if "user" in kwargs:
            user = kwargs["user"]
            del kwargs["user"]
        super().__init__(*args, **kwargs)
        if user != None and not user.is_anonymous:
            datos = user.datos.get_or_create()[0]
            self.fields["nombre"].initial = user.first_name
            self.fields["apellidos"].initial = user.last_name
            self.fields["direccion"].initial = datos.direccion
            self.fields["email"].initial = user.email
            self.fields["metodo_de_pago"].initial = datos.metodo_de_pago

    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    direccion = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    metodo_de_pago = forms.TypedChoiceField(
        choices=[("Contrareembolso", "Contrareembolso"), ("Pasarela","Pasarela de pago")]
    )
    forma_entrega = forms.TypedChoiceField(
        choices=[("Presencialmente", "Presencialmente"), ("Envío","Envío")]
    )

class AdminFormFactura(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['nombre', 'apellidos', 'direccion', 'email', 'metodo_de_pago', 'forma_entrega', 'estado']

    # Personalizando el campo 'email' para que sea 'disabled'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, instance=kwargs["instance"])

        def readonly(*args):
            for atr in args:
                self.fields[atr].widget.attrs['readonly'] = 'readonly'

        def disabled(*args):
            for atr in args:
                self.fields[atr].widget.attrs['disabled'] = 'disabled'

        self.fields['email'].widget = forms.TextInput()
        self.fields['metodo_de_pago'].widget = forms.TextInput()
        self.fields['forma_entrega'].widget = forms.TextInput()
        match self.instance.estado:
            case "Pendiente":
                self.fields['estado'].choices = [("Pendiente","Pendiente"), ("Enviado","Enviado")]
                readonly('nombre', 'apellidos', 'email', 'direccion', 'metodo_de_pago', 'forma_entrega')
            case "Enviado":
                self.fields['estado'].choices = [("Enviado","Enviado"), ("Entregado","Entregado")]
                readonly('nombre', 'apellidos', 'email', 'direccion', 'metodo_de_pago', 'forma_entrega')
            case "Entregado":
                disabled(*self.fields)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"
        