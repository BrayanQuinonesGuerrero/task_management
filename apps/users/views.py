from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import (
    LoginView, LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView
)

from .forms import UserRegistrationForm, UserLoginForm, UserPasswordResetForm, UserPasswordResetConfirmForm

User = get_user_model()


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        self.send_verification_email(user)
        messages.success(self.request, 'Your account has been created. Check your email for verification link.')
        return redirect('users:login')
    
    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account'
        message = render_to_string('users/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
        })  
        send_mail(mail_subject, message, 'noreply@example.com', [user.email])


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Your account has been activated. You can log in now.')
        return redirect('users:login')
    
    else:
        messages.error(request, 'Invalid activation link. Please try again.')
        return redirect('users:register')


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks:task_list')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')


class PasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'users/password_reset/password_reset.html'
    email_template_name = 'users/password_reset/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        associated_users = User.objects.filter(email=email)

        if associated_users.exists():
            return super().form_valid(form)


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset/password_reset_done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserPasswordResetConfirmForm
    template_name = 'users/password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')
    
    def get_success_url(self):
        messages.success(self.request, 'Your password has been reset. Please log in with your new password.')
        return super().get_success_url()