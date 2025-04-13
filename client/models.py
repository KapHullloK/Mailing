from django.db import models

from users.models import User

NULLABLE = {
    'blank': True,
    'null': True,
}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="email")
    full_name = models.CharField(max_length=70, verbose_name="full name", **NULLABLE)
    comment = models.CharField(max_length=300, verbose_name="comment", **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="owner")

    def __str__(self):
        return f"{self.email} {self.full_name}"


class Message(models.Model):
    topic = models.CharField(max_length=100, verbose_name="topic")
    message = models.TextField(verbose_name='message')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="owner")

    def __str__(self):
        return f"{self.topic}"


class Mail(models.Model):
    PERIODICITY_CHOICES = [
        ('day', 'Каждый день'),
        ('week', 'Каждую неделю'),
        ('month', 'Каждый месяц'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('failed', 'Ошибка'),
        ('completed', 'Завершена'),
    ]

    time_for_sending = models.DateTimeField(verbose_name="first mailing date")
    periodicity = models.CharField(max_length=20, choices=PERIODICITY_CHOICES, default='week',
                                   verbose_name="periodicity")
    recipients = models.ManyToManyField(Client, related_name='mails', verbose_name="recipients")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="message")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name="status")
    is_active = models.BooleanField(default=True, verbose_name="is active")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mails', verbose_name="owner")

    def __str__(self):
        return f"{self.pk}"


class Attempt(models.Model):
    last_modified_date = models.DateTimeField(auto_now=True, verbose_name="last modified date")
    mail_response = models.TextField(verbose_name="mail response", **NULLABLE)
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, related_name='attempt', verbose_name='mail')

    def __str__(self):
        return f"{self.pk}"
