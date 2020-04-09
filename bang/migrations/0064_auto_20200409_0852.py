# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0063_auto_20200317_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='alt_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Name (Offstage)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='d_alt_names',
            field=models.TextField(null=True, verbose_name=b'Offstage Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='japanese_alt_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Name (Offstage - Japanese)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='i_school_year',
            field=models.PositiveIntegerField(null=True, verbose_name='School year', choices=[(0, 'First'), (1, 'Second'), (2, 'Third'), (3, 'Junior Third'), (4, 'Junior Second')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='japanese_name',
            field=models.CharField(default='', max_length=100, verbose_name='Name (Japanese)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(unique=True, max_length=100, verbose_name='Name'),
            preserve_default=True,
        ),
    ]
