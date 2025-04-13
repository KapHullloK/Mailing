from django.contrib import admin

from client.models import Client, Mail, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('time_for_sending', 'periodicity', 'message', 'status')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('topic',)
