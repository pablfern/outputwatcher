# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20161113_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='followingoutputs',
            name='user_status',
            field=models.CharField(default=b'pending', max_length=10, verbose_name='Estado seg\xfan usuario', choices=[(b'pending', b'pendiente'), (b'confirmed', b'confirmado')]),
        ),
        migrations.AlterField(
            model_name='followingoutputs',
            name='status',
            field=models.CharField(default=b'watching', max_length=9, verbose_name='Estado', choices=[(b'watching', b'siguiendo'), (b'used', b'usado'), (b'confirmed', b'confirmado')]),
        ),
    ]
