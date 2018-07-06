# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0044_account_level_on_screenshot_upload'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='d_descriptions',
            new_name='d_m_descriptions',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='description',
            new_name='m_description',
        ),
        migrations.AddField(
            model_name='member',
            name='classroom',
            field=models.CharField(max_length=10, null=True, verbose_name='Classroom'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='height',
            field=models.PositiveIntegerField(help_text=b'in cm', null=True, verbose_name='Height'),
            preserve_default=True,
        ),
    ]
