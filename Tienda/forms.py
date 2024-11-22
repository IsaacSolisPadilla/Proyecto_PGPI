from django import forms

class FormFactura(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    direccion = forms.CharField(max_length=255)
    metodo_de_pago = forms.TypedChoiceField(
        choices=[("Contrareembolso", "Contrareembolso"), ("Pasarela","Pasarela de pago")]
    )