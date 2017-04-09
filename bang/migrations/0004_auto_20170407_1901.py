# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0003_auto_20170406_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='skill_details',
            field=models.CharField(max_length=500, null=True, verbose_name='Skill'),
            preserve_default=True,
        ),
    ]
