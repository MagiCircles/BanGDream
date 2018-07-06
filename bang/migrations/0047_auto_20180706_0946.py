# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0046_auto_20180706_0922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='member',
        ),
        migrations.AddField(
            model_name='asset',
            name='members',
            field=models.ManyToManyField(related_name='assets', null=True, verbose_name='Members', to='bang.Member'),
            preserve_default=True,
        ),
    ]
