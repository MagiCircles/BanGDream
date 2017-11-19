# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import web.utils


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0014_auto_20171119_0246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=web.utils.uploadToKeepName(b'images/'))),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='card',
            name='chibi',
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_chibis_ids',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_chibis_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_chibis_paths',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='chibis',
            field=models.ManyToManyField(related_name='chibi', verbose_name='Chibi', to='bang.Image'),
            preserve_default=True,
        ),
    ]
