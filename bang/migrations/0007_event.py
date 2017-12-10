# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bang', '0006_auto_20170409_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'e'), verbose_name='Image')),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('japanese_name', models.CharField(unique=True, max_length=100, verbose_name='Name (Japanese)')),
                ('start_date', models.DateTimeField(null=True, verbose_name='Beginning')),
                ('end_date', models.DateTimeField(null=True, verbose_name='End')),
                ('rare_stamp', models.ImageField(upload_to=magi.utils.uploadItem(b'e/stamps'))),
                ('owner', models.ForeignKey(related_name='added_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
