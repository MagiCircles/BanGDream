# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0043_auto_20180622_0650'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='level_on_screenshot_upload',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
    ]
