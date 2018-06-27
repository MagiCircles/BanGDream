# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0044_member_classroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i'), null=True, verbose_name='Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='square_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'i/m'), null=True, verbose_name='Image'),
            preserve_default=True,
        ),
    ]
