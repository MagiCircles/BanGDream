# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0026_auto_20180225_0304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='_cache_event_last_update',
            new_name='_cache_events_last_update',
        ),
        migrations.RenameField(
            model_name='card',
            old_name='_cache_gacha_last_update',
            new_name='_cache_gachas_last_update',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_event_id',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_event_image',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_event_japanese_name',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_event_name',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_gacha_id',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_gacha_image',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_gacha_japanese_name',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_gacha_name',
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_j_events',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_j_gachas',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='boost_members',
            field=models.ManyToManyField(related_name='boost_in_events', verbose_name='Boost members', to='bang.Member'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='i_boost_attribute',
            field=models.PositiveIntegerField(null=True, verbose_name='Boost attribute', choices=[(1, 'Power'), (2, 'Cool'), (3, 'Pure'), (4, 'Happy')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='rare_stamp',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/stamps'), null=True, verbose_name='Rare stamp'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='stamp_translation',
            field=models.CharField(max_length=200, null=True, verbose_name='Stamp translation'),
            preserve_default=True,
        ),
    ]
