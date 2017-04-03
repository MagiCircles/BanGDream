# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='hobbies',
            field=models.CharField(max_length=100, null=True, verbose_name='Instrument'),
            preserve_default=True,
        ),
    ]
