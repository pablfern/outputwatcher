# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMessage


def output_in_tx_email(output, index, transaction, to_emails, **kwargs):
    body = "El output " + output + u" con índice " + index + u" fue utilizado en la transacción " + transaction + "."
    email = EmailMessage("Uno de los outputs que estabas siguiendo fue utilizado", body,
                         settings.EMAIL_HOST_USER,
                         to_emails, **kwargs)
    email.content_subtype = 'html'
    email.send()
    