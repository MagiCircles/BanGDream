# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0017_auto_20171202_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='_cache_leaderboard',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_leaderboards_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_color',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_email',
            field=models.EmailField(max_length=75, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_preferences_i_status',
            field=models.CharField(max_length=12, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_preferences_twitter',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_username',
            field=models.CharField(max_length=32, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='level',
            field=models.PositiveIntegerField(null=True, verbose_name='Level'),
            preserve_default=True,
        ),
    ]
