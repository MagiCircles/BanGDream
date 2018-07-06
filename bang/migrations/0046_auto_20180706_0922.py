# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0045_auto_20180706_0507'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='source',
            field=models.CharField(max_length=100, null=True, verbose_name='Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='source_link',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='asset',
            name='i_type',
            field=models.PositiveIntegerField(null=True, verbose_name=b'Type', choices=[(0, 'Comics'), (1, 'Backgrounds'), (2, 'Stamps'), (3, 'Titles'), (4, 'Interface'), (5, 'Official art')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(help_text=b'plural', max_length=100, null=True, verbose_name='Title'),
            preserve_default=True,
        ),
    ]
