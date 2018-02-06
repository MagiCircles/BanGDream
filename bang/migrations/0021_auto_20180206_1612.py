# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0020_auto_20180204_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='is_promo',
            field=models.BooleanField(default=False, verbose_name='Promo card'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='c_versions',
            field=models.TextField(default=b'"JP"', null=True, verbose_name='Available in versions', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='english_end_date',
            field=models.DateTimeField(null=True, verbose_name='English version - End'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='english_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/e'), null=True, verbose_name='English version - Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='english_start_date',
            field=models.DateTimeField(null=True, verbose_name='English version - Beginning'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='i_type',
            field=models.PositiveIntegerField(default=0, verbose_name='Event type', choices=[(0, 'Normal'), (1, 'Challenge Live'), (2, 'Band Battle'), (3, 'Live Trial')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='korean_end_date',
            field=models.DateTimeField(null=True, verbose_name='Korean version - End'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='korean_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/t'), null=True, verbose_name='Korean version - Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='korean_start_date',
            field=models.DateTimeField(null=True, verbose_name='Korean version - Beginning'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='taiwanese_end_date',
            field=models.DateTimeField(null=True, verbose_name='Taiwanese version - End'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='taiwanese_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/t'), null=True, verbose_name='Taiwanese version - Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='taiwanese_start_date',
            field=models.DateTimeField(null=True, verbose_name='Taiwanese version - Beginning'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='is_trial_master_completed',
            field=models.NullBooleanField(verbose_name='Trial master completed'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='is_trial_master_ex_completed',
            field=models.NullBooleanField(verbose_name='Trial master EX completed'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='c_versions',
            field=models.TextField(default=b'"JP"', null=True, verbose_name='Available in versions', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='english_end_date',
            field=models.DateTimeField(null=True, verbose_name='English version - End'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='english_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/e'), null=True, verbose_name='English version - Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='english_start_date',
            field=models.DateTimeField(null=True, verbose_name='English version - Beginning'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='korean_end_date',
            field=models.DateTimeField(null=True, verbose_name='Korean version - End'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='korean_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/t'), null=True, verbose_name='Korean version - Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='korean_start_date',
            field=models.DateTimeField(null=True, verbose_name='Korean version - Beginning'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='limited',
            field=models.BooleanField(default=False, verbose_name='Limited'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='taiwanese_end_date',
            field=models.DateTimeField(null=True, verbose_name='Taiwanese version - End'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='taiwanese_image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/t'), null=True, verbose_name='Taiwanese version - Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gacha',
            name='taiwanese_start_date',
            field=models.DateTimeField(null=True, verbose_name='Taiwanese version - Beginning'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playedsong',
            name='screenshot',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'song_screenshot'), null=True, verbose_name='Screenshot'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='c_versions',
            field=models.TextField(default=b'"JP"', null=True, verbose_name='Available in versions', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Join date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='nickname',
            field=models.CharField(help_text="Give a nickname to your account to easily differentiate it from your other accounts when you're managing them.", max_length=200, null=True, verbose_name='Nickname'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='Japanese version - End'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='Japanese version - Beginning'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gacha',
            name='i_attribute',
            field=models.PositiveIntegerField(null=True, verbose_name='Attribute', choices=[(1, 'Power'), (2, 'Cool'), (3, 'Pure'), (4, 'Happy')]),
            preserve_default=True,
        ),
    ]
