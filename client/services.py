import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

scheduler = None


def send_emails() -> None:
    from client.models import Mail
    from client.models import Attempt
    from Mailing import settings
    from datetime import timedelta
    from django.core.mail import send_mail
    from django.utils import timezone

    now = timezone.now()

    scheduled_mails = Mail.objects.filter(time_for_sending__lte=now, status__in=['created', 'completed'],
                                          is_active=True)

    for mail in scheduled_mails:
        mail.status = 'started'
        mail.save()

    for mail in scheduled_mails:
        recipients = mail.recipients.values_list('email', flat=True)

        try:
            send_mail(
                subject=mail.message.topic,
                message=mail.message.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=list(recipients),
            )

            if mail.periodicity == 'day':
                mail.time_for_sending += timedelta(days=1)
            elif mail.periodicity == 'week':
                mail.time_for_sending += timedelta(weeks=1)
            elif mail.periodicity == 'month':
                mail.time_for_sending += timedelta(days=30)

            mail.status = 'completed'
            mail.save()

        except Exception as e:
            mail.status = 'failed'
            mail.save()
            Attempt.objects.create(mail_response=e, mail=mail)


def start_scheduler() -> None:
    global scheduler
    if scheduler is None or not scheduler.running:
        scheduler = BackgroundScheduler()

        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_emails,
            'interval',
            seconds=20,
            id="send_emails",
            replace_existing=True,
        )

        scheduler.start()
        print("Планировщик запущен!")


def stop_scheduler() -> None:
    global scheduler
    if scheduler and scheduler.running:
        scheduler.shutdown()
        print("Планировщик остановлен.")


atexit.register(stop_scheduler)
