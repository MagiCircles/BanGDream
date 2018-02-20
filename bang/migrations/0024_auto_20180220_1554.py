# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0023_auto_20180217_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='side_skill_details',
        ),
        migrations.RemoveField(
            model_name='card',
            name='skill_details',
        ),
        migrations.AddField(
            model_name='card',
            name='i_skill_note_type',
            field=models.PositiveIntegerField(null=True, verbose_name=b'{note_type}', choices=[(0, b'MISS'), (1, b'BAD'), (2, b'GOOD'), (3, b'GREAT'), (4, b'PERFECT')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='i_skill_special',
            field=models.PositiveIntegerField(null=True, verbose_name=b'Skill details - Special case', choices=[(0, b'Boost score limited to perfect notes'), (1, b'Boost score based on stamina')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='skill_alt_percentage',
            field=models.FloatField(help_text=b'0-100', null=True, verbose_name=b'{alt_percentage}'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='skill_duration',
            field=models.PositiveIntegerField(help_text=b'in seconds', null=True, verbose_name=b'{duration}'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='skill_percentage',
            field=models.FloatField(help_text=b'0-100', null=True, verbose_name=b'{percentage}'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='skill_stamina',
            field=models.PositiveIntegerField(null=True, verbose_name=b'{stamina}'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='c_versions',
            field=models.TextField(default=b'"JP"', null=True, verbose_name='Server availability', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='c_versions',
            field=models.TextField(default=b'"JP"', null=True, verbose_name='Server availability', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gacha',
            name='c_versions',
            field=models.TextField(default=b'"JP"', null=True, verbose_name='Server availability', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='c_versions',
            field=models.TextField(default=b'"JP"', null=True, verbose_name='Server availability', blank=True),
            preserve_default=True,
        ),
    ]
