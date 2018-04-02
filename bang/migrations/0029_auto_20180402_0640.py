# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0028_auto_20180320_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='english_rare_stamp',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/stamps/en'), null=True, verbose_name='Rare stamp'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='korean_rare_stamp',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/stamps/kr'), null=True, verbose_name='Rare stamp'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='taiwanese_rare_stamp',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/stamps/tw'), null=True, verbose_name='Rare stamp'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='d_descriptions',
            field=models.TextField(null=True, verbose_name='Description'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='d_schools',
            field=models.TextField(null=True, verbose_name='School'),
            preserve_default=True,
        ),
    ]
