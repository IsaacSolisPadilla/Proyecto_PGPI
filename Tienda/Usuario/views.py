from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import EditDatosUserForm, EditProfileForm, EditPasswordForm
from django.contrib.auth.models import User
from .forms import EditUserForm
from django.contrib.auth.decorators import user_passes_test

@login_required
def edit_profile(request):
    user = request.user
    datos = user.datos.get_or_create(user=user)[0]
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, instance=user)
        password_form = EditPasswordForm(user=user, data=request.POST)
        datos_form = EditDatosUserForm(request.POST, instance=datos)

        if profile_form.is_valid() and datos_form.is_valid():
            # Guardar datos del perfil
            profile_form.save()
            datos_form.save()

            # Cambiar contraseña si se proporcionaron los datos
            if password_form.is_valid() and password_form.cleaned_data.get('old_password'):
                password_form.save()
                update_session_auth_hash(request, password_form.user)

            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('/')
        else:
            messages.error(request, 'Por favor, corrige los errores.')
    else:
        profile_form = EditProfileForm(instance=user)
        password_form = EditPasswordForm(user=user)
        datos_form = EditDatosUserForm(instance=datos)

    return render(request, 'login/edit_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'datos_form': datos_form
    })

@login_required
def user_list(request):
    # Verifica si el usuario logueado tiene is_staff=True
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    # Obtén todos los usuarios
    users = User.objects.all()
    return render(request, 'login/user_list.html', {'users': users})

def user_is_staff(user):
    return user.is_staff

@login_required
def edit_user(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    user = get_object_or_404(User, id=user_id)  # Obtener al usuario por su ID
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Guardar los cambios en el usuario
            return redirect('user_list')  # Redirigir a la lista de usuarios o a la vista deseada
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = EditUserForm(instance=user)  # Cargar el formulario con los datos actuales del usuario

    return render(request, 'login/edit_user.html', {
        'form': form,
        'user': user
    })

@login_required
def create_new_user(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        is_staff = request.POST.get('is_staff')  # Obtén el valor del checkbox

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                
                # Asigna el rol de staff si el checkbox está marcado
                if is_staff:
                    user.is_staff = True
                else:
                    user.is_staff = False

                user.save()

                return redirect('user_list')  # Redirige a la página principal

            except Exception as e:
                messages.error(request, "Hubo un error al registrarse: " + str(e))
        else:
            messages.error(request, "Las contraseñas no coinciden.")
    
    return render(request, 'login/create_new_user.html')

@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    # Verificar si el usuario está autenticado y tiene permisos para eliminar usuarios
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "No tienes permiso para eliminar usuarios.")
        return redirect('user_list')  # Redirige a la lista de usuarios si no tiene permisos
    
    user = get_object_or_404(User, id=user_id)
    
    try:
        user.delete()
    except Exception as e:
        messages.error(request, f"Hubo un error al intentar eliminar al usuario: {e}")

    return redirect('user_list')