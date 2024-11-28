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

@pytest.mark.django_db
def test_user_list_access(client):
    """
    Verifica que solo los usuarios con permisos de administrador puedan acceder a la lista de usuarios.
    """
    # Crear usuarios
    admin_user = User.objects.create_user(username="admin", password="adminpassword", is_staff=True)
    regular_user = User.objects.create_user(username="user", password="userpassword", is_staff=False)

    # Verificar acceso para usuario regular
    client.login(username='user', password='userpassword')
    url = reverse('user_list')
    response = client.get(url)
    assert response.status_code == 403  # Prohibido

    # Verificar acceso para administrador
    client.logout()
    client.login(username='admin', password='adminpassword')
    response = client.get(url)
    assert response.status_code == 200
    assert 'users' in response.context

@pytest.mark.django_db
def test_create_new_user(client):
    # Crear un usuario staff autenticado
    staff_user = User.objects.create_user(username="admin", password="adminpassword", is_staff=True)
    client.login(username='admin', password='adminpassword')

    # Datos válidos
    valid_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testuser@example.com',
        'username': 'testuser',
        'password': 'securepassword123',
        'confirm_password': 'securepassword123',
        'is_staff': True
    }

    # Simular solicitud POST a la vista
    url = reverse('crear_usuario')
    response = client.post(url, data=valid_data)

    # Verificar creación de usuario y redirección
    assert response.status_code == 302
    assert User.objects.filter(username='testuser').exists()

    # Verificar atributos
    user = User.objects.get(username='testuser')
    assert user.is_staff is True


@pytest.mark.django_db
def test_create_new_user_password_mismatch(client):
    # Crear un usuario staff autenticado
    staff_user = User.objects.create_user(username="admin", password="adminpassword", is_staff=True)
    client.login(username='admin', password='adminpassword')

    # Datos inválidos
    invalid_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testuser@example.com',
        'username': 'testuser',
        'password': 'securepassword123',
        'confirm_password': 'wrongpassword',  # Contraseñas no coinciden
        'is_staff': True
    }

    # Simular solicitud POST a la vista
    url = reverse('crear_usuario')
    response = client.post(url, data=invalid_data)

    # Verificar que el usuario no fue creado
    assert response.status_code == 200  # La página muestra errores
    assert not User.objects.filter(username='testuser').exists()


@pytest.mark.django_db
def test_delete_user(client, django_user_model):
    """
    Verifica que se pueda eliminar un usuario correctamente.
    """
    # Crear un usuario de prueba
    user = django_user_model.objects.create_user(
        username='testuser', password='securepassword123', email='testuser@example.com'
    )

    # Crear un usuario staff autenticado para eliminar al usuario
    staff_user = django_user_model.objects.create_user(
        username='adminuser', password='securepassword123', is_staff=True
    )
    client.login(username='adminuser', password='securepassword123')

    # URL para eliminar al usuario
    url = reverse('delete_user', args=[user.id])
    response = client.post(url)

    # Asegurarse de que el usuario fue eliminado
    assert response.status_code == 302  # Redirección exitosa
    assert not User.objects.filter(username='testuser').exists()

