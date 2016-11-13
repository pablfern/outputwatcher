# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20161113_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='output',
            name='amount',
            field=models.PositiveIntegerField(verbose_name='total'),
        ),
    ]
