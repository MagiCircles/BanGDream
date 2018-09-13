# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0050_auto_20180904_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='i_type',
            field=models.PositiveIntegerField(default=0, verbose_name='Event type', choices=[(0, 'Normal'), (1, 'Challenge Live'), (2, 'VS Live'), (3, 'Live Trial')]),
            preserve_default=True,
        ),
    ]
