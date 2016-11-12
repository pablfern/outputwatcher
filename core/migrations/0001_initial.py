# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowingOutputs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='Fecha de creaci\xf3n')),
            ],
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.PositiveIntegerField(verbose_name='Indice del output')),
                ('amount', models.DecimalField(verbose_name='total', max_digits=16, decimal_places=8)),
                ('spent_index', models.PositiveIntegerField(null=True, verbose_name='Indice de input', blank=True)),
                ('spent_date', models.DateTimeField(null=True, verbose_name='Fecha de utilizaci\xf3n', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_id', models.CharField(unique=True, max_length=100, verbose_name='ID de la transacci\xf3n')),
            ],
        ),
        migrations.AddField(
            model_name='output',
            name='spent_transaction',
            field=models.ForeignKey(related_name='transaction_input', verbose_name='Transacci\xf3n de input', blank=True, to='core.Transaction', null=True),
        ),
        migrations.AddField(
            model_name='output',
            name='transaction',
            field=models.ForeignKey(related_name='transaction_output', verbose_name='Transacci\xf3n', to='core.Transaction'),
        ),
        migrations.AddField(
            model_name='followingoutputs',
            name='output',
            field=models.ForeignKey(to='core.Output'),
        ),
        migrations.AddField(
            model_name='followingoutputs',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='output',
            unique_together=set([('transaction', 'index')]),
        ),
    ]
