# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0064_auto_20200409_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='is_full',
            field=models.BooleanField(default=False, verbose_name=b'FULL'),
            preserve_default=True,
        ),
    ]
