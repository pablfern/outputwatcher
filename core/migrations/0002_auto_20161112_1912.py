# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='output',
            name='address',
            field=models.CharField(max_length=200, null=True, verbose_name='Direcci\xf3n', blank=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='network',
            field=models.CharField(default=b'testnet', max_length=20, choices=[(b'livenet', b'livenet'), (b'testnet', b'testnet')]),
        ),
        migrations.AlterUniqueTogether(
            name='followingoutputs',
            unique_together=set([('user', 'output')]),
        ),
    ]
