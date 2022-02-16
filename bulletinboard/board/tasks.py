from celery import shared_task
from django.core.mail import EmailMultiAlternatives


# celery -A app_my worker -l INFO -B
# Флаг B - периодические задачи

@shared_task
def send_mail(user_email='Test'):
    # pass
    print(f'Отправка уведомления для: {user_email}')
    #
    # msg = EmailMultiAlternatives(
    #     subject=f'Новостной портал News paper: новая публикация',
    #     from_email='a.zaprudnov@abbott.ru',
    #     to=[user_email],
    # )
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()

