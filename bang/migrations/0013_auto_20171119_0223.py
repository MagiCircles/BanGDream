# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0012_song'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='easy_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Easy - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(28)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='expert_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Expert - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(28)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='hard_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Hard - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(28)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='i_unlock',
            field=models.PositiveIntegerField(verbose_name='How to unlock?', choices=[(0, 'Gift'), (1, 'Purchase at CiRCLE'), (2, 'Complete story'), (3, 'Complete Tutorial'), (4, 'Initially available'), (5, 'Other')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='normal_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Normal - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(28)]),
            preserve_default=True,
        ),
    ]
