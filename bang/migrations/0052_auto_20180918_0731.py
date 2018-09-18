# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0051_auto_20180913_0407'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='_tthumbnail_english_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTthumb(b'asset/e')),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='_tthumbnail_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTthumb(b'asset')),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='_tthumbnail_korean_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTthumb(b'asset/k')),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='_tthumbnail_taiwanese_image',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadTthumb(b'asset/t')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='asset',
            name='event',
            field=models.ForeignKey(related_name='assets', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Event', to='bang.Event', null=True),
            preserve_default=True,
        ),
    ]
