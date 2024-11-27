import pytest
from django.contrib.auth.models import User
from Tienda.models import Factura
from Tienda.forms import FormFactura, AdminFormFactura

@pytest.mark.django_db
def test_form_factura_sin_usuario():
    # Inicializar el formulario sin pasar el usuario
    form = FormFactura()

    # Verificar que los valores iniciales sean vacíos
    assert form.fields['nombre'].initial is None
    assert form.fields['apellidos'].initial is None
    assert form.fields['direccion'].initial is None
    assert form.fields['email'].initial is None
    assert form.fields['metodo_de_pago'].initial is None


@pytest.mark.django_db
def test_admin_form_factura_estado_pendiente():
    # Crear una factura con estado 'Pendiente'
    user = User.objects.create_user(username="testuser", password="testpassword", first_name="Juan", last_name="Perez", email="juan@example.com")
    factura = Factura.objects.create(nombre="Juan", apellidos="Perez", direccion="Calle Falsa 123", email="juan@example.com", metodo_de_pago="Contrareembolso", estado="Pendiente", usuario=user)
    
    # Inicializar el formulario de administrador con la factura pendiente
    form = AdminFormFactura(instance=factura)

    # Verificar que el campo 'estado' tenga las opciones correctas
    assert form.fields['estado'].choices == [("Pendiente", "Pendiente"), ("Enviado", "Enviado")]

    # Verificar que los campos 'nombre', 'apellidos', 'direccion' y 'metodo_de_pago' sean readonly
    assert form.fields['nombre'].widget.attrs['readonly'] == 'readonly'
    assert form.fields['apellidos'].widget.attrs['readonly'] == 'readonly'
    assert form.fields['direccion'].widget.attrs['readonly'] == 'readonly'
    assert form.fields['metodo_de_pago'].widget.attrs['readonly'] == 'readonly'


@pytest.mark.django_db
def test_admin_form_factura_estado_enviado():
    # Crear una factura con estado 'Enviado'
    user = User.objects.create_user(username="testuser", password="testpassword", first_name="Juan", last_name="Perez", email="juan@example.com")
    factura = Factura.objects.create(nombre="Juan", apellidos="Perez", direccion="Calle Falsa 123", email="juan@example.com", metodo_de_pago="Contrareembolso", estado="Enviado", usuario=user)
    
    # Inicializar el formulario de administrador con la factura enviada
    form = AdminFormFactura(instance=factura)

    # Verificar que el campo 'estado' tenga las opciones correctas
    assert form.fields['estado'].choices == [("Enviado", "Enviado"), ("Entregado", "Entregado")]

    # Verificar que los campos 'nombre', 'apellidos', 'direccion' y 'metodo_de_pago' sean readonly
    assert form.fields['nombre'].widget.attrs['readonly'] == 'readonly'
    assert form.fields['apellidos'].widget.attrs['readonly'] == 'readonly'
    assert form.fields['direccion'].widget.attrs['readonly'] == 'readonly'
    assert form.fields['metodo_de_pago'].widget.attrs['readonly'] == 'readonly'


@pytest.mark.django_db
def test_admin_form_factura_estado_entregado():
    # Crear una factura con estado 'Entregado'
    user = User.objects.create_user(username="testuser", password="testpassword", first_name="Juan", last_name="Perez", email="juan@example.com")
    factura = Factura.objects.create(nombre="Juan", apellidos="Perez", direccion="Calle Falsa 123", email="juan@example.com", metodo_de_pago="Contrareembolso", estado="Entregado", usuario=user)
    
    # Inicializar el formulario de administrador con la factura entregada
    form = AdminFormFactura(instance=factura)

    # Verificar que todos los campos estén deshabilitados
    assert form.fields['nombre'].widget.attrs['disabled'] == 'disabled'
    assert form.fields['apellidos'].widget.attrs['disabled'] == 'disabled'
    assert form.fields['direccion'].widget.attrs['disabled'] == 'disabled'
    assert form.fields['metodo_de_pago'].widget.attrs['disabled'] == 'disabled'
    assert form.fields['estado'].widget.attrs['disabled'] == 'disabled'
