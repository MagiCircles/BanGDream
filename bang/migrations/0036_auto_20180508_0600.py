# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0035_auto_20180504_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='i_band',
            field=models.PositiveIntegerField(verbose_name='Band', choices=[(0, b"Poppin' Party"), (1, b'Afterglow'), (2, b'Pastel*Palettes'), (3, b'Roselia'), (4, b'Hello, Happy World!')]),
            preserve_default=True,
        ),
    ]
