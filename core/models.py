# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    NETWORKS = [('livenet', 'livenet'), ('testnet', 'testnet')]
    transaction_id = models.CharField(unique=True,
                                      max_length=100, 
                                      verbose_name=u"ID de la transacción")
    transaction_index = models.PositiveIntegerField(null=True, blank=True, verbose_name=u'BlockChain transaction index')
    network = models.CharField(max_length=20, default='testnet', choices=NETWORKS)
    confirmed_date = models.DateTimeField(null=True, blank=True, verbose_name=u'Fecha de confirmación')
    
    def __unicode__(self):
        return "{} - {}".format(self.transaction_id, self.network)


class Output(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='transaction_output', verbose_name=u'Transacción')
    index = models.PositiveIntegerField(verbose_name=u'Indice del output')
    amount = models.PositiveIntegerField(verbose_name=u'total')
    spent_transaction = models.ForeignKey(Transaction, null=True, blank=True, related_name='transaction_input', verbose_name=u'Transacción de input')
    spent_index = models.PositiveIntegerField(null=True, blank=True, verbose_name=u'Indice de input')
    spent_date = models.DateTimeField(null=True, blank=True, verbose_name=u'Fecha de utilización')
    script = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'Script')

    class Meta:
        unique_together = ('transaction', 'index', )

    def __unicode__(self):
        return "{} - {} - {}".format(self.transaction.transaction_id, 
                                self.index,
                                self.amount)


class FollowingOutputs(models.Model):
    STATUS = [('watching', 'siguiendo'), 
              ('used', 'usado'),
              ('confirmed', 'confirmado')]
    USER_STATUS = [('pending', 'pendiente'), 
                    ('confirmed', 'confirmado')]
    user = models.ForeignKey(User)
    output = models.ForeignKey(Output)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=u'Fecha de creación')
    status = models.CharField(max_length=9, default='watching', choices=STATUS, verbose_name=u'Estado')
    user_status = models.CharField(max_length=10, default='pending', choices=USER_STATUS, verbose_name=u'Estado según usuario')
    
    class Meta:
        unique_together = ('user', 'output', )

    def __unicode__(self):
        return "{} - {} - {}".format(self.status, self.user.email, self.output)
