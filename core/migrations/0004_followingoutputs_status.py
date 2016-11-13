# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_output_script'),
    ]

    operations = [
        migrations.AddField(
            model_name='followingoutputs',
            name='status',
            field=models.CharField(default=b'watching', max_length=9, verbose_name='Estado'),
        ),
    ]
