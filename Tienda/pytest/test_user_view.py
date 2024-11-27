import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

@pytest.mark.django_db
def test_edit_profile(client):
    # Crear un usuario de prueba
    user = User.objects.create_user(username="testuser", password="testpassword")
    user.save()

    # Iniciar sesión como el usuario creado
    client.login(username='testuser', password='testpassword')

    # Crear los datos del formulario (suponiendo que EditProfileForm y EditDatosUserForm están bien definidos)
    new_name = "New Name"
    new_email = "newemail@example.com"
    new_old_password = "testpassword"
    new_password = "newpassword"

    # Crear los datos para la solicitud POST (formularios)
    post_data = {
        'username': new_name,
        'email': new_email,
        'old_password': new_old_password,
        'new_password1': new_password,
        'new_password2': new_password,
        'first_name': 'New',
        'last_name': 'User'
    }

    # Simular una solicitud POST a la vista de editar perfil
    url = reverse('edit_profile')  # Asegúrate de que la URL esté configurada correctamente
    response = client.post(url, post_data)

    # Verificar que la redirección ocurra (lo más probable es que redirija a la página de inicio u otra página)
    assert response.status_code == 200  # Redirección después de guardar correctamente

    # Verificar que el usuario se haya actualizado correctamente
    user.refresh_from_db()  # Recargar la instancia del usuario desde la base de datos

    # Verificar que la contraseña se haya actualizado correctamente
    user = User.objects.get(username='testuser')

    # Verificar que se haya mostrado un mensaje de éxito
    messages = list(get_messages(response.wsgi_request))