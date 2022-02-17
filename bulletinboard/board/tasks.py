from celery import shared_task
from django.core.mail import EmailMultiAlternatives


# celery -A app_my worker -l INFO -B
# Флаг B - периодические задачи
@shared_task()
def send_mail(from_email, to_emails, subjects_email, html_content):

    msg = EmailMultiAlternatives(
        subject=subjects_email,
        from_email=from_email,
        to=to_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
