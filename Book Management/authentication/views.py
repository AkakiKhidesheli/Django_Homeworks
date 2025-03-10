from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView, \
    PasswordResetView
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
import logging
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import CreateView

# Create your views here.

logger = logging.getLogger(__name__)

class RegisterUserView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')

class LoginUserView(LoginView):
    template_name = 'registration/login.html'

class LogoutUserView(LogoutView):
    next_page = reverse_lazy('book_list')

class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    login_url = reverse_lazy('login')
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('book_list')

class ResetPasswordView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('login')

class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirmation.html'
    success_url = reverse_lazy('login')

# def register_user(request):
#     logger.info(f"Started Registering User, IP: {request.META.get('REMOTE_ADDR')}")
#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             logger.info(f"Registered user '{form.cleaned_data["username"]}', IP: {request.META.get('REMOTE_ADDR')}")
#             return redirect('book_list')
#         else:
#             logger.error(f"Invalid form, IP: {request.META.get('REMOTE_ADDR')}")
#             return render(request, 'registration/registration.html', {'form': form})
#
#     else:
#         form = RegistrationForm()
#         return render(request, 'registration/registration.html', {'form': form})


# def login_user(request):
#     logger.info(f"Started Login, IP: {request.META.get('REMOTE_ADDR')}")
#     if request.method == "POST":
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#
#             user = authenticate(request, username=username, password=password)
#
#             if user is not None:
#                 login(request, user)
#                 logger.info(f"Logged in user '{username}', IP: {request.META.get('REMOTE_ADDR')}")
#                 return redirect('book_list')
#
#     else:
#         form = AuthenticationForm()
#
#     return render(request, 'registration/login.html', {'form': form})

#
# def logout_user(request):
#     logger.info(f"Logging out user '{request.user}', IP: {request.META.get('REMOTE_ADDR')}")
#     logout(request)
#     logger.info(f"Logged out user, IP: {request.META.get('REMOTE_ADDR')}")
#     return redirect('book_list')

# @login_required(login_url='login')
# def change_password(request):
#     if request.method == "POST":
#         form = PasswordChangeForm(user=request.user, data=request.POST)
#         if form.is_valid():
#             form.save()
#
#             update_session_auth_hash(request, request.user)
#
#             return redirect('book_list')
#         else:
#             return render(request, 'registration/change_password.html', {'form': form})
#     else:
#         form = PasswordChangeForm(user=request.user)
#
#         return render(request, 'registration/change_password.html', {'form': form})


# def reset_password(request):
#     if request.method == "POST":
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data["email"]
#             if not User.objects.filter(email=email).exists():
#                 messages.error(request, "User with this email does not exist.")
#                 return redirect("reset_password")
#             form.save(
#                 request = request,
#                 use_https = False,
#                 email_template_name = 'registration/password_reset_email.html',
#             )
#             messages.success(request, 'Password reset form is sent. Please, check your email')
#             return redirect('reset_password')
#     else:
#         form = PasswordResetForm()
#         return render(request, 'registration/password_reset.html', {'form': form})


# def reset_password_confirm(request, uidb64, token):
#     try:
#         id = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(id=id)
#
#         if default_token_generator.check_token(user, token):
#             if request.method == "POST":
#                 form = SetPasswordForm(user=user, data=request.POST)
#                 if form.is_valid():
#                     form.save()
#
#                     return redirect('login')
#             else:
#                 form = SetPasswordForm(user=user)
#         else:
#             messages.error(request, 'Invalid Password.')
#             return redirect('/')
#
#     except (ValueError, TypeError, User.DoesNotExist):
#         messages.error(request, f'Invalid mail.')
#         return redirect('/')
#
#     return render(request, 'registration/password_reset_confirmation.html', {'form': form})
