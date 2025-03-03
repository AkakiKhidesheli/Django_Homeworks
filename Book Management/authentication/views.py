from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
import logging

# Create your views here.

logger = logging.getLogger(__name__)

def register_user(request):
    logger.info(f"Started Registering User, IP: {request.META.get('REMOTE_ADDR')}")
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            logger.info(f"Registered user '{form.cleaned_data["username"]}', IP: {request.META.get('REMOTE_ADDR')}")
            return redirect('book_list')
        else:
            logger.error(f"Invalid form, IP: {request.META.get('REMOTE_ADDR')}")
            return render(request, 'registration/registration.html', {'form': form})

    else:
        form = RegistrationForm()
        return render(request, 'registration/registration.html', {'form': form})


def login_user(request):
    logger.info(f"Started Login, IP: {request.META.get('REMOTE_ADDR')}")
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                logger.info(f"Logged in user '{username}', IP: {request.META.get('REMOTE_ADDR')}")
                return redirect('book_list')

    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    logger.info(f"Logging out user '{request.user}', IP: {request.META.get('REMOTE_ADDR')}")
    logout(request)
    logger.info(f"Logged out user, IP: {request.META.get('REMOTE_ADDR')}")
    return redirect('book_list')

@login_required(login_url='login')
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()

            update_session_auth_hash(request, request.user)

            return redirect('book_list')
        else:
            return render(request, 'registration/change_password.html', {'form': form})
    else:
        form = PasswordChangeForm(user=request.user)

        return render(request, 'registration/change_password.html', {'form': form})


# def reset_password(request):
#     if request.method == "POST":
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             form.save(
#                 request = request,
#                 use_https = False,
#                 email_template_name = 'registration/password_reset_email.html',
#             )