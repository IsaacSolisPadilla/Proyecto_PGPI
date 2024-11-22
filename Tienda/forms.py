from django import forms

from Tienda.models import Factura

class FormFactura(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    direccion = forms.CharField(max_length=255)
    metodo_de_pago = forms.TypedChoiceField(
        choices=[("Contrareembolso", "Contrareembolso"), ("Pasarela","Pasarela de pago")]
    )

class AdminFormFactura(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['nombre', 'apellidos', 'direccion', 'metodo_de_pago', 'estado']

    # Personalizando el campo 'email' para que sea 'disabled'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, instance=kwargs["instance"])

        def readonly(*args):
            for atr in args:
                self.fields[atr].widget.attrs['readonly'] = 'readonly'

        def disabled(*args):
            for atr in args:
                self.fields[atr].widget.attrs['disabled'] = 'disabled'

        self.fields['metodo_de_pago'].widget = forms.TextInput()
        match self.instance.estado:
            case "Espera" | "Entregado":
                self.fields['estado'].widget.attrs['readonly'] = 'readonly'
                disabled(*self.fields)
            case "Pendiente":
                self.fields['estado'].choices = [("Pendiente","Pendiente"), ("Enviado","Enviado")]
                readonly('nombre', 'apellidos', 'direccion', 'metodo_de_pago')
            case "Enviado":
                self.fields['estado'].choices = [("Enviado","Enviado"), ("Entregado","Entregado")]
                readonly('nombre', 'apellidos', 'direccion', 'metodo_de_pago')
        


        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"
        