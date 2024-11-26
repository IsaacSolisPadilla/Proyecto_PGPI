from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import EditDatosUserForm, EditProfileForm, EditPasswordForm

@login_required
def edit_profile(request):
    user = request.user
    datos = user.datos.get()
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
