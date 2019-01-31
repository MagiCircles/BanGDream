# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0058_auto_20181210_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areaitem',
            name='i_boost_stat',
            field=models.PositiveIntegerField(null=True, verbose_name='Statistic', choices=[(0, 'Performance'), (1, 'Technique'), (2, 'Visual')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='areaitem',
            name='i_type',
            field=models.PositiveIntegerField(null=True, verbose_name='Area', choices=[(0, 'Studio'), (1, 'Poster'), (2, 'Counter'), (3, 'Mini table'), (4, 'Magazine rack'), (5, 'Entrance'), (6, 'Sign'), (7, 'Plaza'), (8, 'Garden'), (9, 'Specials menu')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='areaitem',
            name='max_level',
            field=models.PositiveIntegerField(default=5, verbose_name='Max level'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_side_skill_type',
            field=models.PositiveIntegerField(db_index=True, null=True, verbose_name=b'Side skill', choices=[(1, 'Score up'), (2, 'Life recovery'), (3, 'Perfect lock'), (4, 'Life guard')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_skill_special',
            field=models.PositiveIntegerField(null=True, verbose_name=b'Skill details - Special case', choices=[(0, b'Based off PERFECT notes'), (1, b'Scoreup based on stamina'), (2, b'Better scoreup if you can hit perfects')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_skill_type',
            field=models.PositiveIntegerField(db_index=True, null=True, verbose_name='Skill', choices=[(1, 'Score up'), (2, 'Life recovery'), (3, 'Perfect lock'), (4, 'Life guard')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='collectiblecard',
            name='max_leveled',
            field=models.NullBooleanField(verbose_name='Max level'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='i_boost_stat',
            field=models.PositiveIntegerField(null=True, verbose_name='Boost statistic', choices=[(0, 'Performance'), (1, 'Technique'), (2, 'Visual')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='i_type',
            field=models.PositiveIntegerField(null=True, verbose_name='Type', choices=[(0, 'Main'), (1, 'Live boost'), (2, 'Studio ticket'), (3, 'Other')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='i_school_year',
            field=models.PositiveIntegerField(null=True, verbose_name='School year', choices=[(0, 'First'), (1, 'Second'), (2, 'Junior Third')]),
            preserve_default=True,
        ),
    ]
