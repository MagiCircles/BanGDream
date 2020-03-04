# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0061_auto_20190513_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='start_date',
            field=models.DateField(null=True, verbose_name='Start date', validators=[magi.utils.PastOnlyValidator]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='asset',
            name='i_band',
            field=models.PositiveIntegerField(help_text=b"Tagging a band is a shortcut to tagging all the members, so you don't need to tag the members when you tag a band.", null=True, verbose_name='Band', choices=[(0, b"Poppin'Party"), (1, b'Afterglow'), (2, b'Pastel*Palettes'), (3, b'Roselia'), (4, b'Hello, Happy World!'), (5, b'RAISE A SUILEN'), (6, b'Morfonica')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='i_band',
            field=models.PositiveIntegerField(null=True, verbose_name='Band', choices=[(0, b"Poppin'Party"), (1, b'Afterglow'), (2, b'Pastel*Palettes'), (3, b'Roselia'), (4, b'Hello, Happy World!'), (5, b'RAISE A SUILEN'), (6, b'Morfonica')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='i_band',
            field=models.PositiveIntegerField(verbose_name='Band', choices=[(0, b"Poppin'Party"), (1, b'Afterglow'), (2, b'Pastel*Palettes'), (3, b'Roselia'), (4, b'Hello, Happy World!'), (5, b'RAISE A SUILEN'), (6, b'Morfonica'), (7, b'Glitter*Green'), (8, b'Special Band')]),
            preserve_default=True,
        ),
    ]
