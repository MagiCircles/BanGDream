# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import web.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bang', '0007_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gacha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=web.utils.uploadItem(b'g'), verbose_name='Image')),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('japanese_name', models.CharField(unique=True, max_length=100, verbose_name='Name (Japanese)')),
                ('start_date', models.DateTimeField(null=True, verbose_name='Beginning')),
                ('end_date', models.DateTimeField(null=True, verbose_name='End')),
                ('i_attribute', models.PositiveIntegerField(verbose_name='Attribute', choices=[(1, 'Power'), (2, 'Cool'), (3, 'Pure'), (4, 'Happy')])),
                ('cards', models.ManyToManyField(related_name='gachas', verbose_name=b'Cards', to='bang.Card')),
                ('event', models.ForeignKey(related_name='gachas', verbose_name='Event', to='bang.Event')),
                ('owner', models.ForeignKey(related_name='added_gacha', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_event_id',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_event_image',
            field=models.ImageField(null=True, upload_to=web.utils.uploadItem(b'e')),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_event_japanese_name',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_event_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_event_name',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='i_side_skill_type',
            field=models.PositiveIntegerField(null=True, verbose_name='Side skill', choices=[(1, 'Score Up'), (2, 'Life Recovery'), (3, 'Perfect Lock')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='side_skill_details',
            field=models.CharField(max_length=500, null=True, verbose_name='Side skill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='boost_members',
            field=models.ManyToManyField(related_name='boost_in_events', verbose_name='Boost Members', to='bang.Member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='i_boost_attribute',
            field=models.PositiveIntegerField(null=True, verbose_name='Boost Attribute', choices=[(1, 'Power'), (2, 'Cool'), (3, 'Pure'), (4, 'Happy')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='main_card',
            field=models.ForeignKey(related_name='main_card_event', to='bang.Card', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='secondary_card',
            field=models.ForeignKey(related_name='secondary_card_event', to='bang.Card', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='stamp_translation',
            field=models.CharField(max_length=200, null=True, verbose_name='Stamp Translation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='rare_stamp',
            field=models.ImageField(upload_to=web.utils.uploadItem(b'e/stamps'), verbose_name='Rare Stamp'),
            preserve_default=True,
        ),
    ]
