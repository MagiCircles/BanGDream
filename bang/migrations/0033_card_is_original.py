# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0032_card_cameo_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='is_original',
            field=models.BooleanField(default=False, verbose_name='Original card'),
            preserve_default=True,
        ),
    ]
