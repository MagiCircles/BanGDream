# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0045_auto_20180620_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='height',
            field=models.PositiveIntegerField(help_text='in cm', null=True, verbose_name='Height'),
            preserve_default=True,
        ),
    ]
