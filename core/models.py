# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    NETWORKS = [('livenet', 'livenet'), ('testnet', 'testnet')]
    transaction_id = models.CharField(unique=True,
                                      max_length=100, 
                                      verbose_name=u"ID de la transacción")
    network = models.CharField(max_length=20, default='testnet', choices=NETWORKS)

    def __unicode__(self):
        return "{} - {}".format(self.transaction_id, self.network)


class Output(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='transaction_output', verbose_name=u'Transacción')
    index = models.PositiveIntegerField(verbose_name=u'Indice del output')
    amount = models.DecimalField(max_digits=16, decimal_places=8, verbose_name=u'total')
    spent_transaction = models.ForeignKey(Transaction, null=True, blank=True, related_name='transaction_input', verbose_name=u'Transacción de input')
    spent_index = models.PositiveIntegerField(null=True, blank=True, verbose_name=u'Indice de input')
    spent_date = models.DateTimeField(null=True, blank=True, verbose_name=u'Fecha de utilización')
    script = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'Script')
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'Dirección') #S criptPubKey['address']    

    class Meta:
        unique_together = ('transaction', 'index', )

    def __unicode__(self):
        return "{} - {}".format(self.transaction.transaction_id, 
                                self.index)


class FollowingOutputs(models.Model):
    STATUS = [('watching', 'siguiendo'), 
              ('notified', 'notificado'),
              ('confirmed', 'confirmado')]
    user = models.ForeignKey(User)
    output = models.ForeignKey(Output)
    creation_date = models.DateTimeField(verbose_name=u'Fecha de creación')
    status = models.CharField(max_length=9, default='watching', verbose_name=u'Estado')
    
    class Meta:
        unique_together = ('user', 'output', )

    def __unicode__(self):
        return "{} - {} - {}".format(self.status, self.user.email, self.output)
