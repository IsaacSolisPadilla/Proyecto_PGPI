import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from cart.cart import Cart
from Tienda.models import CategoriaProducto, Producto, Datos

@pytest.mark.django_db
def test_login_view_success(client):
    user = User.objects.create_user(username="testuser", email="testuser@example.com", password="password123")
    response = client.post(reverse('login'), {'email': 'testuser@example.com', 'password': 'password123'})
    assert response.status_code == 302  # Redirect after login
    assert response.url == '/'  # Redirect to home page

@pytest.mark.django_db
def test_login_view_invalid_email(client):
    response = client.post(reverse('login'), {'email': 'invalid@example.com', 'password': 'password123'})
    assert response.status_code == 302  # Redirect after failed login
    assert response.url == reverse('login')  # Redirect to login page

@pytest.mark.django_db
def test_register_view_success(client):
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'username': 'johndoe',
        'password': 'securepassword123',
        'confirm_password': 'securepassword123',
    }
    response = client.post(reverse('register'), data)
    assert response.status_code == 302  # Redirect after successful registration
    assert response.url == '/'  # Redirect to home page
    assert User.objects.filter(username='johndoe').exists()

@pytest.mark.django_db
def test_register_view_password_mismatch(client):
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'username': 'johndoe',
        'password': 'securepassword123',
        'confirm_password': 'differentpassword',
    }
    response = client.post(reverse('register'), data)
    assert response.status_code == 302  # Redirect after failed registration
    assert response.url == reverse('register')  # Redirect to register page

