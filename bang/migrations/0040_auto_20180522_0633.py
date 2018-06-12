# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import magi.utils

def move_card_live2d_model_pkg(apps, schema_editor):
    Card = apps.get_model('bang', 'Card')
    Costume = apps.get_model('bang', 'Costume')

    migd = 0
    for card in Card.objects.select_related('member').filter(live2d_model_pkg__isnull=False).order_by('id'):
        if not card.live2d_model_pkg:
            continue

        costume = Costume()
        costume.owner_id = card.owner_id
        costume.i_costume_type = 0 # get_i('costume_type', 'live')
        costume.card = card
        costume.member = card.member
        costume.model_pkg = card.live2d_model_pkg
        costume.preview_image = card.live2d_screenshot
        costume.save()
        migd += 1

    print('move_card_live2d_model_pkg: created', migd, 'new costume objects', end='')


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bang', '0039_auto_20180520_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='Costume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('i_costume_type', models.PositiveIntegerField(verbose_name='Costume type', choices=[(0, b'live'), (1, b'other')])),
                ('name', models.CharField(max_length=250, null=True, verbose_name='Name')),
                ('d_names', models.TextField(null=True, verbose_name='Name')),
                ('preview_image', models.ImageField(upload_to=magi.utils.uploadItem(b'cos/p'), null=True, verbose_name='Image')),
                ('model_pkg', models.FileField(upload_to=magi.utils.uploadItem(b'cos/z'), verbose_name='Model')),
                ('card', models.OneToOneField(related_name='associated_costume', null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='Card', to='bang.Card')),
                ('member', models.ForeignKey(related_name='associated_costume', verbose_name='Member', to='bang.Member', null=True)),
                ('owner', models.ForeignKey(related_name='added_costume', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='member',
            name='_cache_total_costumes',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.RunPython(move_card_live2d_model_pkg),
        migrations.RemoveField(
            model_name='card',
            name='_tthumbnail_live2d_screenshot',
        ),
        migrations.RemoveField(
            model_name='card',
            name='live2d_model_pkg',
        ),
        migrations.RemoveField(
            model_name='card',
            name='live2d_screenshot',
        ),
        migrations.AddField(
            model_name='costume',
            name='_tthumbnail_preview_image',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
    ]
