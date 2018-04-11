# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0030_auto_20180403_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventparticipation',
            name='screenshot',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'event_screenshot'), null=True, verbose_name='Screenshot'),
            preserve_default=True,
        ),
    ]
