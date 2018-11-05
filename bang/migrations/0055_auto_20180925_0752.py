# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0054_asset_song'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_hidden_from_leaderboard',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'Hide from leaderboard'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='is_playground',
            field=models.BooleanField(default=False, db_index=True, verbose_name='Playground'),
            preserve_default=True,
        ),
    ]
