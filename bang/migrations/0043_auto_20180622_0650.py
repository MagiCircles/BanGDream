# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0042_auto_20180613_0711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rerun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('i_version', models.PositiveIntegerField(verbose_name='Version', choices=[(0, 'Japanese version'), (1, 'English version'), (2, 'Taiwanese version'), (3, 'Korean version')])),
                ('start_date', models.DateTimeField(verbose_name='Beginning')),
                ('end_date', models.DateTimeField(verbose_name='End')),
                ('event', models.ForeignKey(related_name='reruns', verbose_name='Event', to='bang.Event', null=True)),
                ('gacha', models.ForeignKey(related_name='reruns', verbose_name='Gacha', to='bang.Gacha', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='costume',
            name='i_costume_type',
            field=models.PositiveIntegerField(verbose_name='Costume type', choices=[(0, 'Live'), (1, 'Other')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='easy_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Easy - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(40)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='expert_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Expert - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(40)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='hard_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Hard - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(40)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='normal_difficulty',
            field=models.PositiveIntegerField(null=True, verbose_name='Normal - Difficulty', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(40)]),
            preserve_default=True,
        ),
    ]
