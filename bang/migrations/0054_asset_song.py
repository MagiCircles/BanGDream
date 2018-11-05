# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0053_auto_20180918_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='song',
            field=models.ForeignKey(related_name='assets', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Song', to='bang.Song', null=True),
            preserve_default=True,
        ),
    ]
