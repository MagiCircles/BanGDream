# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0005_auto_20170409_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='level',
            field=models.PositiveIntegerField(null=True, verbose_name='Level', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(200)]),
            preserve_default=True,
        ),
    ]
