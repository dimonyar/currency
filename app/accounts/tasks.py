import datetime

from accounts.models import User

from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


@shared_task
def send_activation_email(username: str, email: str):
    subject = 'Sign Up'
    message_body = f'''
            Activation Link:
            {settings.HTTP_SCHEMA}://{settings.DOMAIN}{reverse('accounts:activate-user', args=[username])}
            '''
    email_from = settings.EMAIL_HOST_USER
    send_mail(
        subject,
        message_body,
        email_from,
        [email],
        fail_silently=False,
    )


@shared_task
def new_users():
    subject = f'''Count of Users of Currency-service achieved {count_users()}'''
    message_body = user_list()
    send_mail(
        subject,
        message_body,
        'support@currency.com',
        ['dy@rteam.net.ua'],
        fail_silently=False,
    )


def count_users():
    return str(User.objects.filter(is_active=True).count())


def user_list():
    query = User.objects.filter(is_active=True,
                                date_joined__gte=(datetime.datetime.now() + datetime.timedelta(days=-7)))
    lst = [(i.first_name, i.last_name, i.email, i.date_joined.strftime("%m/%d/%Y")) for i in query]
    return '\n'.join(map(str, lst))
