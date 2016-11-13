# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20161112_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='output',
            name='script',
            field=models.CharField(max_length=200, null=True, verbose_name='Script', blank=True),
        ),
    ]
