# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0056_auto_20181008_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='skill_alt_stamina',
            field=models.PositiveIntegerField(null=True, verbose_name=b'{alt_stamina}'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_skill_special',
            field=models.PositiveIntegerField(null=True, verbose_name=b'Skill details - Special case', choices=[(0, b'Based off PERFECT notes'), (1, b'Scoreup based on stamina')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='costume',
            name='d_names',
            field=models.TextField(null=True, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='costume',
            name='name',
            field=models.CharField(max_length=250, null=True, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='i_type',
            field=models.PositiveIntegerField(default=0, verbose_name='Event type', choices=[(0, 'Normal'), (1, 'Challenge Live'), (2, 'VS Live'), (3, 'Live Trial'), (4, 'Mission Live')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='c_unlock_variables',
            field=models.CharField(max_length=100, null=True, verbose_name='How to unlock?'),
            preserve_default=True,
        ),
    ]
