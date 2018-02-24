# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0024_auto_20180220_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectiblecard',
            name='prefer_untrained',
            field=models.BooleanField(default=False, verbose_name='Prefer untrained card image'),
            preserve_default=True,
        ),
    ]
