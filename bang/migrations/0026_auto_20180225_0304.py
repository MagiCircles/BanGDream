# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0025_collectiblecard_prefer_untrained'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='rare_stamp',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/stamps'), null=True, verbose_name='Rare Stamp'),
            preserve_default=True,
        ),
    ]
