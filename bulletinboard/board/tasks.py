import datetime

from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User as UserDjango

from bulletinboard.settings import get_env

from .models import Ad


def datetime_range(cur_datetime):

    cur_datetime = datetime.time(cur_datetime.hour, cur_datetime.minute, cur_datetime.second)

    perf_range = ['вечер и ночь', 'утро и день', 'конец дня']

    range_day = {
        1: (datetime.time(0, 0, 0), datetime.time(8, 0, 0)),
        2: (datetime.time(8, 0, 0), datetime.time(16, 0, 0)),
        3: (datetime.time(16, 0, 0), datetime.time(0, 0, 0)),
    }

    range_cur = 0
    for range_cur in range_day:
        if range_day[range_cur][0] <= cur_datetime < range_day[range_cur][1]:
            print(f'Текущее время: {cur_datetime}')
            print(f'Начало: {range_day[range_cur][0]}')
            print(f'Конец: {range_day[range_cur][1]}')
            start = datetime.datetime.combine(datetime.datetime.today(), range_day[range_cur][0], tzinfo=None)
            if range_cur == 3:
                end = datetime.datetime.combine(datetime.datetime.today() + datetime.timedelta(days=1), range_day[range_cur][1], tzinfo=None)
            else:
                end = datetime.datetime.combine(datetime.datetime.today(), range_day[range_cur][1], tzinfo=None)
            break

    print(f'Начало: {start}')
    print(f'Конец: {end}')

    dict_ = {
        'perf_range': perf_range[range_cur - 1],
        'range': [start, end]
    }

    return dict_


# celery -A app_my worker -l INFO -B
# Флаг B - периодические задачи
@shared_task
def send_mail(from_email, to_emails, subjects_email, html_content):

    msg = EmailMultiAlternatives(
        subject=subjects_email,
        from_email=from_email,
        to=to_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def news_everyday():

    dict_ = datetime_range(datetime.datetime.utcnow().time())
    perf_range = dict_['perf_range']

    ads = Ad.objects.filter(
        datetime_created__range=dict_['range'],
        type_ad_news=True
    )

    if ads:
        users = UserDjango.objects.all()

        text_body = ''
        for news in ads:
            text_body += news.title + '<br>'
            text_body += f'http://127.0.0.1:8000/ad_detail/{news.id}<br>'
            text_body += '<hr>'
            text_body += '<br>'

        email_hu = get_env('EMAIL_HOST_USER')
        subject = 'Рассылка свежих новостей за сегодня'

        html_content = render_to_string(
            'board/respone_mail.html',
            {
                'text_title': f'Свежие новости за {perf_range}',
                'date_time': f'Дата публикации: {datetime.datetime.utcnow().strftime("%d/%m/%y")}',
                'text_body': f'Сообщение: "{text_body}"',
                'text_contacts': f'Электронная почта: {email_hu}',
                'mailing': True,
            }
        )

        for user_ in users:
            print(f'{user_.email}')

            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=email_hu,
                to=[user_.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

