# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0010_auto_20171108_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='friend_id',
            field=models.PositiveIntegerField(null=True, verbose_name='Friend ID'),
            preserve_default=True,
        ),
    ]
