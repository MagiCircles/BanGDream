# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0029_auto_20180402_0640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collectiblecard',
            name='_cache_account_owner_id',
        ),
        migrations.RemoveField(
            model_name='collectiblecard',
            name='_cache_account_unicode',
        ),
        migrations.RemoveField(
            model_name='eventparticipation',
            name='_cache_account_owner_id',
        ),
        migrations.RemoveField(
            model_name='eventparticipation',
            name='_cache_account_unicode',
        ),
        migrations.RemoveField(
            model_name='playedsong',
            name='_cache_account_owner_id',
        ),
        migrations.RemoveField(
            model_name='playedsong',
            name='_cache_account_unicode',
        ),
        migrations.AddField(
            model_name='collectiblecard',
            name='_cache_j_account',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='_cache_j_account',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playedsong',
            name='_cache_j_account',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='english_rare_stamp',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/stamps/en'), null=True, verbose_name='English version - Rare stamp'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='korean_rare_stamp',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/stamps/kr'), null=True, verbose_name='Korean version - Rare stamp'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='taiwanese_rare_stamp',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'e/stamps/tw'), null=True, verbose_name='Taiwanese version - Rare stamp'),
            preserve_default=True,
        ),
    ]
