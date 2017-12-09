# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import web.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0015_auto_20171119_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='art_trained',
            field=models.ImageField(upload_to=web.utils.uploadItem(b'c/art/a'), null=True, verbose_name='Art (Trained)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='image_trained',
            field=models.ImageField(upload_to=web.utils.uploadItem(b'c/a'), null=True, verbose_name='Icon (Trained)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='transparent_trained',
            field=models.ImageField(upload_to=web.utils.uploadItem(b'c/transparent/a'), null=True, verbose_name='Transparent (Trained)'),
            preserve_default=True,
        ),
    ]
