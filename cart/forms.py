from django import forms


class CartAddProductForm(forms.Form):
    cantidad = forms.IntegerField(
        required=False,
        initial=1,
        min_value=1
    )
    sobreescribir = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        stock = kwargs.pop('stock', None)
        super().__init__(*args, **kwargs)
        if stock is not None:
            self.fields['cantidad'].widget.attrs['max'] = stock