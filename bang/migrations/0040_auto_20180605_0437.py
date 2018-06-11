# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0039_auto_20180520_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='_thumbnail_screenshot',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadThumb(b'account_screenshot')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='area',
            name='_original_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'areas')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='areaitem',
            name='_original_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'areas/items')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='asset',
            name='_original_english_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'asset/e')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='asset',
            name='_original_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'asset')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='asset',
            name='_original_korean_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'asset/k')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='asset',
            name='_original_taiwanese_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'asset/t')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_2x_art',
            field=models.ImageField(null=True, upload_to=magi.utils.upload2x(b'c/art')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_2x_art_trained',
            field=models.ImageField(null=True, upload_to=magi.utils.upload2x(b'c/art/a')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_2x_transparent',
            field=models.ImageField(null=True, upload_to=magi.utils.upload2x(b'c/transparent')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_2x_transparent_trained',
            field=models.ImageField(null=True, upload_to=magi.utils.upload2x(b'c/transparent/a')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_original_art',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'c/art')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_original_art_trained',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'c/art/a')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_original_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'c')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_original_image_trained',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'c/a')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_tthumbnail_art',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTthumb(b'c/art')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_tthumbnail_art_trained',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTthumb(b'c/art/a')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_tthumbnail_transparent',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTthumb(b'c/transparent')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_tthumbnail_transparent_trained',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTthumb(b'c/transparent/a')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='_original_english_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'e/e')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='_original_english_rare_stamp',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'e/stamps/en')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='_original_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'e')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='_original_korean_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'e/t')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='_original_korean_rare_stamp',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'e/stamps/kr')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='_original_rare_stamp',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'e/stamps')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='_original_taiwanese_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'e/t')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='_original_taiwanese_rare_stamp',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'e/stamps/tw')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventparticipation',
            name='_thumbnail_screenshot',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadThumb(b'event_screenshot')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gacha',
            name='_original_english_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'e/e')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gacha',
            name='_original_korean_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'e/t')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gacha',
            name='_original_screenshot',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'g')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gacha',
            name='_original_taiwanese_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'e/t')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='_original_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'items')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='_original_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'i')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='_original_square_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'i/m')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='playedsong',
            name='_thumbnail_screenshot',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadThumb(b'song_screenshot')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='_original_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b's')),
            preserve_default=True,
        ),
    ]
