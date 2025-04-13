from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from client.forms import ClientForm, MessageForm, MailForm, MailManagerForm
from client.models import Client, Message, Mail


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    context_object_name = 'clients'
    login_url = reverse_lazy('users:login')


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:clients_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:clients_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients:clients_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'messages'
    login_url = reverse_lazy('users:login')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        for message in context['messages']:
            message.message = message.message[:50]

        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('message:message_list')


class MailListView(LoginRequiredMixin, ListView):
    model = Mail
    context_object_name = 'mails'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.groups.filter(name='Managers').exists():
            return Mail.objects.all()

        return Mail.objects.filter(owner=user)


class MailCreateView(LoginRequiredMixin, CreateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mail:mail_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailUpdateView(LoginRequiredMixin, UpdateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mail:mail_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_class(self):
        user = self.request.user

        if user == self.object.owner or user.is_superuser:
            return MailForm
        elif user.groups.filter(name='Managers').exists():
            return MailManagerForm
        return PermissionDenied


class MailDeleteView(LoginRequiredMixin, DeleteView):
    model = Mail
    success_url = reverse_lazy('mail:mail_list')
