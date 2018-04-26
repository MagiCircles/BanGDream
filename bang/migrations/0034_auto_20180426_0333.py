# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0033_card_is_original'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='show_art_on_homepage',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='show_trained_art_on_homepage',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
