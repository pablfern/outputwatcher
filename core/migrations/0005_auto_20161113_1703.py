# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_followingoutputs_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='output',
            name='address',
        ),
        migrations.AddField(
            model_name='transaction',
            name='confirmed_date',
            field=models.DateTimeField(null=True, verbose_name='Fecha de confirmaci\xf3n', blank=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_index',
            field=models.PositiveIntegerField(null=True, verbose_name='BlockChain transaction index', blank=True),
        ),
        migrations.AlterField(
            model_name='followingoutputs',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creaci\xf3n'),
        ),
    ]
