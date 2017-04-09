# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0004_auto_20170407_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='japanese_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Title (Japanese)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='Title'),
            preserve_default=True,
        ),
    ]
