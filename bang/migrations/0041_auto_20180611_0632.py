# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0040_auto_20180605_0437'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gacha',
            old_name='_original_screenshot',
            new_name='_original_image',
        ),
    ]
