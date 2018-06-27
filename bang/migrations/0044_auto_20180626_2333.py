# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0043_auto_20180620_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='classroom',
            field=models.CharField(max_length=10, null=True, verbose_name='Classroom'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='height',
            field=models.PositiveIntegerField(help_text='in cm', null=True, verbose_name='Height'),
            preserve_default=True,
        ),
    ]
