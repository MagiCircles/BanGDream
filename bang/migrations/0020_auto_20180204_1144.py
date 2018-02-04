# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0019_auto_20180105_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='device',
            field=models.CharField(help_text='The model of your device. Example: Nexus 5, iPhone 4, iPad 2, ...', max_length=150, null=True, verbose_name='Device'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='i_os',
            field=models.PositiveIntegerField(null=True, verbose_name='Operating System', choices=[(0, b'Android'), (1, b'iOs')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='i_play_with',
            field=models.PositiveIntegerField(null=True, verbose_name='Play with', choices=[(0, 'Thumbs'), (1, 'All fingers'), (2, 'Index fingers'), (3, 'One hand'), (4, 'Other')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='i_version',
            field=models.PositiveIntegerField(default=0, verbose_name='Version', choices=[(0, 'Japanese version'), (1, 'English version'), (2, 'Taiwanese version'), (3, 'Korean version')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='screenshot',
            field=models.ImageField(help_text='In-game profile screenshot', upload_to=magi.utils.uploadItem(b'account_screenshot'), null=True, verbose_name='Screenshot'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='stargems_bought',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='c_versions',
            field=models.TextField(default=b'"JP"', null=True, verbose_name='Available in versions', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Join ate'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='nickname',
            field=models.CharField(help_text="Give a nickname to your account to easily differenciate it from your other accounts when you're managing them.", max_length=200, null=True, verbose_name='Nickname'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='start_date',
            field=models.DateField(null=True, verbose_name='Start date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='art',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'c/art'), null=True, verbose_name='Art'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_side_skill_type',
            field=models.PositiveIntegerField(null=True, verbose_name='Side skill', choices=[(1, 'Score up'), (2, 'Life recovery'), (3, 'Perfect lock')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_skill_type',
            field=models.PositiveIntegerField(null=True, verbose_name='Skill', choices=[(1, 'Score up'), (2, 'Life recovery'), (3, 'Perfect lock')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'c'), null=True, verbose_name='Icon'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='transparent',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'c/transparent'), null=True, verbose_name='Transparent'),
            preserve_default=True,
        ),
    ]
