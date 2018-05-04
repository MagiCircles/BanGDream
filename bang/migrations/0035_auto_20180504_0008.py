# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0034_auto_20180426_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='gacha',
            name='dreamfes',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='d_hobbiess',
            field=models.TextField(null=True, verbose_name='Hobbies'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='hobbies',
            field=models.CharField(max_length=100, null=True, verbose_name='Hobbies'),
            preserve_default=True,
        ),
    ]
