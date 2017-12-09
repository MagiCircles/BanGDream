# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0013_auto_20171119_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='event',
            field=models.ForeignKey(related_name='gift_songs', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Event', to='bang.Event', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='i_unlock',
            field=models.PositiveIntegerField(verbose_name='How to unlock?', choices=[(0, 'Gift'), (1, 'Purchase at CiRCLE'), (2, 'Complete story'), (3, 'Complete Tutorial'), (4, 'Initially available'), (5, 'Event gift'), (6, 'Other')]),
            preserve_default=True,
        ),
    ]
