# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0021_auto_20180206_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectiblecard',
            name='_cache_account_unicode',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collectiblecard',
            name='skill_level',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Skill level', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='_cache_account_unicode',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playedsong',
            name='_cache_account_unicode',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
