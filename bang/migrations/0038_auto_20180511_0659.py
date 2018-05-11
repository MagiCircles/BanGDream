# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0037_card_live2d_model_pkg'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='_cache_total_collectedcards',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_total_collectedcards_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_total_favorited',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_total_favorited_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='live2d_screenshot',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadItem(b'c/l2d/s')),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='_cache_total_participations',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='_cache_total_participations_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playedsong',
            name='all_perfect',
            field=models.NullBooleanField(verbose_name='All perfect'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='_cache_total_played',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='_cache_total_played_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
