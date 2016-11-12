# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMessage


def send_email(subject, body, to_emails, **kwargs):
    email = EmailMessage(subject,
                         body,
                         settings.EMAIL_HOST_USER,
                         to_emails, **kwargs)

    email.content_subtype = 'html'
    email.send()