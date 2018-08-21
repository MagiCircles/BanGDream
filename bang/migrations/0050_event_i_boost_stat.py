# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0049_auto_20180818_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='i_boost_stat',
            field=models.PositiveIntegerField(null=True, verbose_name='Boost stat', choices=[(0, 'Performance'), (1, 'Technique'), (2, 'Visual')]),
            preserve_default=True,
        ),
    ]
