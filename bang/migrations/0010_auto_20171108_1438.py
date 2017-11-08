# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import web.utils
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0009_auto_20171106_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='_cache_gacha_id',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_gacha_image',
            field=models.ImageField(null=True, upload_to=web.utils.uploadItem(b'e')),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_gacha_japanese_name',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_gacha_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_gacha_name',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='chibi',
            field=models.ImageField(upload_to=web.utils.uploadItem(b'c/c'), null=True, verbose_name='Chibi'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='level',
            field=models.PositiveIntegerField(null=True, verbose_name='Level', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(300)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='japanese_name',
            field=models.CharField(unique=True, max_length=100, verbose_name='Title (Japanese)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(unique=True, max_length=100, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='i_school_year',
            field=models.PositiveIntegerField(null=True, verbose_name='School Year', choices=[(0, 'First'), (1, 'Second'), (2, 'Junior Third')]),
            preserve_default=True,
        ),
    ]
