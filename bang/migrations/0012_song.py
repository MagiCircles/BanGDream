# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import magi.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bang', '0011_account_friend_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b's'), verbose_name='Album cover')),
                ('i_band', models.PositiveIntegerField(verbose_name='Band', choices=[(0, b"Poppin' Party"), (1, b'Afterglow'), (2, b'Pastel*Palettes'), (3, b'Roselia'), (4, b'Hello, Happy World!')])),
                ('japanese_name', models.CharField(unique=True, max_length=100, verbose_name='Title')),
                ('romaji_name', models.CharField(max_length=100, null=True, verbose_name='Title (Romaji)')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Translation (English)')),
                ('itunes_id', models.PositiveIntegerField(help_text=b'iTunes ID', null=True, verbose_name='Preview')),
                ('length', models.PositiveIntegerField(null=True, verbose_name='Length')),
                ('is_cover', models.BooleanField(default=False, verbose_name='Cover song')),
                ('bpm', models.PositiveIntegerField(null=True, verbose_name='Beats per minute')),
                ('release_date', models.DateField(null=True, verbose_name='Release date')),
                ('composer', models.CharField(max_length=100, null=True, verbose_name='Composer')),
                ('lyricist', models.CharField(max_length=100, null=True, verbose_name='Lyricist')),
                ('arranger', models.CharField(max_length=100, null=True, verbose_name='Arranger')),
                ('easy_notes', models.PositiveIntegerField(null=True, verbose_name='Easy - Notes')),
                ('easy_difficulty', models.PositiveIntegerField(null=True, verbose_name='Easy - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(26)])),
                ('normal_notes', models.PositiveIntegerField(null=True, verbose_name='Normal - Notes')),
                ('normal_difficulty', models.PositiveIntegerField(null=True, verbose_name='Normal - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(26)])),
                ('hard_notes', models.PositiveIntegerField(null=True, verbose_name='Hard - Notes')),
                ('hard_difficulty', models.PositiveIntegerField(null=True, verbose_name='Hard - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(26)])),
                ('expert_notes', models.PositiveIntegerField(null=True, verbose_name='Expert - Notes')),
                ('expert_difficulty', models.PositiveIntegerField(null=True, verbose_name='Expert - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(26)])),
                ('i_unlock', models.PositiveIntegerField(verbose_name='How to unlock?', choices=[(0, 'Gift'), (1, 'Purchase at CiRCLE'), (2, 'Complete story'), (3, 'Complete Tutorial'), (4, 'Other')])),
                ('c_unlock_variables', models.CharField(max_length=100, null=True)),
                ('owner', models.ForeignKey(related_name='added_songs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
