# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMessage


def output_in_tx_email(out_transaction, in_transaction, index, to_emails, **kwargs):
    body = "El output " + str(index) + u" de la transacción " + out_transaction + u"fue gastado en la transacción " + in_transaction
    email = EmailMessage("Uno de los outputs que estabas siguiendo fue utilizado", body,
                         settings.EMAIL_HOST_USER,
                         to_emails, **kwargs)
    email.content_subtype = 'html'
    email.send()


def output_in_confirmed_tx_email(output, index, transaction, to_emails, **kwargs):
    body = u"La transacción " + transaction + u" que seguías con el Output con índice" + str(index) + "fue confirmada en el nuevo bloque de la cadena." 
    email = EmailMessage("La transaccion de uno de los outputs que estabas siguiendo fue confirmada", body,
                         settings.EMAIL_HOST_USER,
                         to_emails, **kwargs)
    email.content_subtype = 'html'
    email.send()
