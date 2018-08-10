# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0047_auto_20180706_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='special_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Special - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='special_notes',
            field=models.PositiveIntegerField(null=True, verbose_name='Special - Notes'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='playedsong',
            name='i_difficulty',
            field=models.PositiveIntegerField(default=0, verbose_name='Difficulty', choices=[(0, 'Easy'), (1, 'Normal'), (2, 'Hard'), (3, 'Expert'), (4, 'Special')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='easy_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Easy - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='expert_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Expert - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='hard_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Hard - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='normal_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Normal - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)]),
            preserve_default=True,
        ),
    ]
