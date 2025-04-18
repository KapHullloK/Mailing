from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView

from Mailing.settings import EMAIL_HOST_USER
from users.forms import UserRegistrationForm, UserBanForm, UserProfileForm
from users.models import User

import secrets


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        url = f'http://{self.request.get_host()}/users/confirm/{token}/'

        send_mail(
            subject="Подтверждение почты",
            message=f"ссылка для подтверждения почты:{url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    context_object_name = 'users'
    login_url = reverse_lazy('users:login')

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='Managers').exists()

    def get_queryset(self):
        return User.objects.annotate(mail_count=Count('mails')).filter(
            is_superuser=False,
            groups__isnull=True
        )


class UserBanView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserBanForm
    success_url = reverse_lazy('users:list_users')

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='Managers').exists()


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile_user', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)

        new_password = form.cleaned_data.get('new_password')
        if new_password:
            update_session_auth_hash(self.request, self.object)

        return response
