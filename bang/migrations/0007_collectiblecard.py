# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0006_auto_20170409_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectibleCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('trained', models.BooleanField(default=False, verbose_name='Trained')),
                ('max_leveled', models.NullBooleanField(verbose_name='Max Leveled')),
                ('first_episode', models.NullBooleanField(verbose_name='1st episode')),
                ('memorial_episode', models.NullBooleanField(verbose_name='Memorial episode')),
                ('account', models.ForeignKey(related_name='cardscollectors', verbose_name='Account', to='bang.Account')),
                ('card', models.ForeignKey(related_name='collectedcards', verbose_name='Card', to='bang.Card')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
