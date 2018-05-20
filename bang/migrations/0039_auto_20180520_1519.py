# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bang', '0038_auto_20180511_0659'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_original_image', models.ImageField(null=True, upload_to=b'')),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'areas'), verbose_name='Image')),
                ('name', models.CharField(max_length=100, verbose_name='Title')),
                ('d_names', models.TextField(null=True, verbose_name='Title')),
                ('owner', models.ForeignKey(related_name='added_areas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AreaItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('i_type', models.PositiveIntegerField(verbose_name=b'Type', choices=[(0, b'Instrument per member'), (1, b'Instrument per band'), (2, 'Poster'), (3, 'Flyer'), (4, 'Food'), (5, 'Decoration'), (6, 'Other')])),
                ('_original_image', models.ImageField(null=True, upload_to=b'')),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'areas/items'), verbose_name='Image')),
                ('value', models.FloatField(null=True)),
                ('flat', models.BooleanField(default=False, help_text=b'Default: Percentage', verbose_name=b'Flat value')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Title')),
                ('d_names', models.TextField(null=True, verbose_name='Title')),
                ('i_band', models.PositiveIntegerField(null=True, verbose_name='Band', choices=[(0, b"Poppin' Party"), (1, b'Afterglow'), (2, b'Pastel*Palettes'), (3, b'Roselia'), (4, b'Hello, Happy World!')])),
                ('i_attribute', models.PositiveIntegerField(null=True, verbose_name='Attribute', choices=[(1, 'Power'), (2, 'Cool'), (3, 'Pure'), (4, 'Happy')])),
                ('instrument', models.CharField(max_length=100, null=True, verbose_name='Instrument')),
                ('d_instruments', models.TextField(null=True, verbose_name='Instrument')),
                ('i_stat', models.PositiveIntegerField(null=True, verbose_name=b'Statistics', choices=[(0, 'Performance'), (1, 'Technique'), (2, 'Visual')])),
                ('depends_on_life', models.PositiveIntegerField(null=True)),
                ('area', models.ForeignKey(verbose_name='Area', to='bang.Area', null=True)),
                ('member', models.ForeignKey(related_name='area_items', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Member', to='bang.Member', null=True)),
                ('owner', models.ForeignKey(related_name='added_area_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_original_image', models.ImageField(null=True, upload_to=b'')),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'asset'), null=True, verbose_name='Image')),
                ('_original_english_image', models.ImageField(null=True, upload_to=b'')),
                ('english_image', models.ImageField(upload_to=magi.utils.uploadItem(b'asset/e'), null=True, verbose_name='English version - Image')),
                ('_original_taiwanese_image', models.ImageField(null=True, upload_to=b'')),
                ('taiwanese_image', models.ImageField(upload_to=magi.utils.uploadItem(b'asset/t'), null=True, verbose_name='Taiwanese version - Image')),
                ('_original_korean_image', models.ImageField(null=True, upload_to=b'')),
                ('korean_image', models.ImageField(upload_to=magi.utils.uploadItem(b'asset/k'), null=True, verbose_name='Korean version - Image')),
                ('i_type', models.PositiveIntegerField(null=True, verbose_name=b'Type', choices=[(0, 'Comics'), (1, 'Backgrounds'), (2, 'Stamps'), (3, 'Titles'), (4, 'Interface')])),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Title')),
                ('d_names', models.TextField(null=True, verbose_name='Title')),
                ('i_band', models.PositiveIntegerField(null=True, verbose_name='Band', choices=[(0, b"Poppin' Party"), (1, b'Afterglow'), (2, b'Pastel*Palettes'), (3, b'Roselia'), (4, b'Hello, Happy World!')])),
                ('c_tags', models.TextField(null=True, verbose_name='Tags')),
                ('value', models.PositiveIntegerField(null=True)),
                ('event', models.ForeignKey(related_name='titles', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Event', to='bang.Event', null=True)),
                ('member', models.ForeignKey(related_name='stamps', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Member', to='bang.Member', null=True)),
                ('owner', models.ForeignKey(related_name='added_assets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollectibleAreaItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_cache_account_last_update', models.DateTimeField(null=True)),
                ('_cache_j_account', models.TextField(null=True)),
                ('level', models.PositiveIntegerField(default=1, verbose_name='Level')),
                ('account', models.ForeignKey(related_name='areaitems', verbose_name='Account', to='bang.Account')),
                ('areaitem', models.ForeignKey(related_name='collectedby', verbose_name='Area item', to='bang.AreaItem')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollectibleItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_cache_account_last_update', models.DateTimeField(null=True)),
                ('_cache_j_account', models.TextField(null=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('account', models.ForeignKey(related_name='items', verbose_name='Account', to='bang.Account')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_original_image', models.ImageField(null=True, upload_to=b'')),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'items'), verbose_name='Image')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Title')),
                ('d_names', models.TextField(null=True, verbose_name='Title')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('d_descriptions', models.TextField(null=True, verbose_name='Description')),
                ('owner', models.ForeignKey(related_name='added_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='collectibleitem',
            name='item',
            field=models.ForeignKey(related_name='collectedby', verbose_name='Item', to='bang.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_thumbnail_screenshot',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_2x_art',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_2x_art_trained',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_2x_transparent',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_2x_transparent_trained',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_original_art',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_original_art_trained',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_original_image',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_original_image_trained',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_tthumbnail_art',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_tthumbnail_art_trained',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_tthumbnail_live2d_screenshot',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_tthumbnail_transparent',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_tthumbnail_transparent_trained',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='_original_english_image',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='_original_english_rare_stamp',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='_original_image',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='_original_korean_image',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='_original_korean_rare_stamp',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='_original_rare_stamp',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='_original_taiwanese_image',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='_original_taiwanese_rare_stamp',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='_thumbnail_screenshot',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='_original_english_image',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='_original_korean_image',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='_original_screenshot',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='_original_taiwanese_image',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='_original_image',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='_original_square_image',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playedsong',
            name='_thumbnail_screenshot',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='_original_image',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
    ]
