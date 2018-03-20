# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0027_auto_20180306_1002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='food_dislikes',
            new_name='food_dislike',
        ),
        migrations.RenameField(
            model_name='member',
            old_name='food_likes',
            new_name='food_like',
        ),
        migrations.RenameField(
            model_name='member',
            old_name='hobbies',
            new_name='instrument',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_member_image',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_member_japanese_name',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_member_name',
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_j_member',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='d_names',
            field=models.TextField(null=True, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='d_skill_names',
            field=models.TextField(null=True, verbose_name='Skill name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='d_names',
            field=models.TextField(null=True, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='d_stamp_translations',
            field=models.TextField(null=True, verbose_name='Stamp translation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='d_names',
            field=models.TextField(null=True, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='d_food_dislikes',
            field=models.TextField(null=True, verbose_name='Disliked food'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='d_food_likes',
            field=models.TextField(null=True, verbose_name='Liked food'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='d_instruments',
            field=models.TextField(null=True, verbose_name='Instrument'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='d_names',
            field=models.TextField(null=True, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='d_names',
            field=models.TextField(null=True, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gacha',
            name='japanese_name',
            field=models.CharField(unique=True, max_length=100, verbose_name='Title (Japanese)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gacha',
            name='name',
            field=models.CharField(unique=True, max_length=100, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(unique=True, max_length=100, verbose_name='Name (Romaji)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='Title (Translation)'),
            preserve_default=True,
        ),
    ]
