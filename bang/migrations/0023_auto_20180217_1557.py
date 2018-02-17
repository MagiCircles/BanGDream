# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0022_auto_20180215_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='release_date',
            field=models.DateField(null=True, verbose_name='Release date', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_attribute',
            field=models.PositiveIntegerField(db_index=True, verbose_name='Attribute', choices=[(1, 'Power'), (2, 'Cool'), (3, 'Pure'), (4, 'Happy')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_rarity',
            field=models.PositiveIntegerField(db_index=True, verbose_name='Rarity', choices=[(1, '\u2605'), (2, '\u2605\u2605'), (3, '\u2605\u2605\u2605'), (4, '\u2605\u2605\u2605\u2605')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_side_skill_type',
            field=models.PositiveIntegerField(db_index=True, null=True, verbose_name='Side skill', choices=[(1, 'Score up'), (2, 'Life recovery'), (3, 'Perfect lock')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_skill_type',
            field=models.PositiveIntegerField(db_index=True, null=True, verbose_name='Skill', choices=[(1, 'Score up'), (2, 'Life recovery'), (3, 'Perfect lock')]),
            preserve_default=True,
        ),
    ]
