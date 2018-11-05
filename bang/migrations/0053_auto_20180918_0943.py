# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0052_auto_20180918_0731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='_original_english_image',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='_original_image',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='_original_korean_image',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='_original_taiwanese_image',
        ),
        migrations.RemoveField(
            model_name='event',
            name='_original_english_rare_stamp',
        ),
        migrations.RemoveField(
            model_name='event',
            name='_original_korean_rare_stamp',
        ),
        migrations.RemoveField(
            model_name='event',
            name='_original_rare_stamp',
        ),
        migrations.RemoveField(
            model_name='event',
            name='_original_taiwanese_rare_stamp',
        ),
        migrations.RemoveField(
            model_name='event',
            name='d_stamp_translations',
        ),
        migrations.RemoveField(
            model_name='event',
            name='english_rare_stamp',
        ),
        migrations.RemoveField(
            model_name='event',
            name='korean_rare_stamp',
        ),
        migrations.RemoveField(
            model_name='event',
            name='rare_stamp',
        ),
        migrations.RemoveField(
            model_name='event',
            name='stamp_translation',
        ),
        migrations.RemoveField(
            model_name='event',
            name='taiwanese_rare_stamp',
        ),
    ]
