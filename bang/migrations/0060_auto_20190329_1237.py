# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0059_auto_20190122_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='i_unlock',
            field=models.PositiveIntegerField(verbose_name='How to unlock?', choices=[(0, 'Gift'), (1, 'Purchase at CiRCLE'), (2, 'Complete story'), (3, 'Complete Tutorial'), (4, 'Initially available'), (5, 'Event gift'), (6, 'Level'), (7, 'Level / Band'), (8, 'Other')]),
            preserve_default=True,
        ),
    ]
