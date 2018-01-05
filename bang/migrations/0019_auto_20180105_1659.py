# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bang', '0018_auto_20171221_1547'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectibleCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_cache_account_last_update', models.DateTimeField(null=True)),
                ('_cache_account_owner_id', models.PositiveIntegerField(null=True)),
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
        migrations.CreateModel(
            name='EventParticipation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_cache_account_last_update', models.DateTimeField(null=True)),
                ('_cache_account_owner_id', models.PositiveIntegerField(null=True)),
                ('score', models.PositiveIntegerField(null=True, verbose_name='Score')),
                ('ranking', models.PositiveIntegerField(null=True, verbose_name='Ranking')),
                ('song_score', models.PositiveIntegerField(null=True, verbose_name='Song score')),
                ('song_ranking', models.PositiveIntegerField(null=True, verbose_name='Song ranking')),
                ('account', models.ForeignKey(related_name='events', verbose_name='Account', to='bang.Account')),
                ('event', models.ForeignKey(related_name='participations', verbose_name='Event', to='bang.Event')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FavoriteCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('card', models.ForeignKey(related_name='favorited', verbose_name='Card', to='bang.Card')),
                ('owner', models.ForeignKey(related_name='favorite_cards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayedSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_cache_account_last_update', models.DateTimeField(null=True)),
                ('_cache_account_owner_id', models.PositiveIntegerField(null=True)),
                ('i_difficulty', models.PositiveIntegerField(default=0, verbose_name='Difficulty', choices=[(0, 'Easy'), (1, 'Normal'), (2, 'Hard'), (3, 'Expert')])),
                ('score', models.PositiveIntegerField(null=True, verbose_name='Score')),
                ('full_combo', models.NullBooleanField(verbose_name='Full combo')),
                ('account', models.ForeignKey(related_name='playedsong', verbose_name='Account', to='bang.Account')),
                ('song', models.ForeignKey(related_name='playedby', verbose_name='Song', to='bang.Song')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='favoritecard',
            unique_together=set([('owner', 'card')]),
        ),
        migrations.AddField(
            model_name='account',
            name='center',
            field=models.ForeignKey(related_name='center_of_account', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Center', to='bang.CollectibleCard', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='default_tab',
            field=models.CharField(max_length=100, null=True, verbose_name='Default tab'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='nickname',
            field=models.CharField(help_text="Give a nickname to your new account to easily differenciate it from your other accounts when you're managing them.", max_length=200, null=True, verbose_name='Nickname'),
            preserve_default=True,
        ),
    ]
