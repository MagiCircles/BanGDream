# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0002_auto_20170402_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='start_date',
            field=models.DateField(null=True, verbose_name='Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Join Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_cache_member_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadItem(b'member')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='i_band',
            field=models.PositiveIntegerField(verbose_name='Band', choices=[(0, b"Poppin' Party"), (1, b'Afterglow'), (2, b'Pastel*Palettes'), (3, b'Roselia'), (4, b'Hello, Happy World!')]),
            preserve_default=True,
        ),
    ]
