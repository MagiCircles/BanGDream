# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0060_auto_20190329_1237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='_cache_totals_last_update',
            new_name='_cache_total_fans_last_update',
        ),
        migrations.RemoveField(
            model_name='member',
            name='_cache_total_cards',
        ),
        migrations.RemoveField(
            model_name='member',
            name='_cache_total_costumes',
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e'), null=True, verbose_name='Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gacha',
            name='image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'g'), null=True, verbose_name='Image'),
            preserve_default=True,
        ),
    ]
