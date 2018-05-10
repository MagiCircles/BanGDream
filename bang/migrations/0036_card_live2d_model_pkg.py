# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0035_auto_20180504_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='live2d_model_pkg',
            field=models.FileField(upload_to=magi.utils.uploadItem(b'c/l2d'), null=True, verbose_name='Live2D'),
            preserve_default=True,
        ),
    ]
