# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0008_auto_20171106_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='main_card',
            field=models.ForeignKey(related_name='main_card_event', on_delete=django.db.models.deletion.SET_NULL, to='bang.Card', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='secondary_card',
            field=models.ForeignKey(related_name='secondary_card_event', on_delete=django.db.models.deletion.SET_NULL, to='bang.Card', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gacha',
            name='event',
            field=models.ForeignKey(related_name='gachas', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Event', to='bang.Event', null=True),
            preserve_default=True,
        ),
    ]
