# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone
import magi.utils

def move_card_chibis(apps, schema_editor):
    Card = apps.get_model('bang', 'Card')
    Costume = apps.get_model('bang', 'Costume')
    NewChibi = apps.get_model('bang', 'Chibi')

    for card in Card.objects.all().select_related('associated_costume').order_by('id'):
        chibis = card.chibis.all()
        if not chibis:
            continue

        if hasattr(card, 'associated_costume'):
            costume = card.associated_costume
        else:
            costume = Costume()
            costume.owner_id = card.owner_id
            costume.i_costume_type = 0 # get_i('costume_type', 'live')
            costume.card = card
            costume.member = card.member
            costume.save()

        for the_image in card.chibis.all():
            new_chibi = NewChibi()
            new_chibi.image = the_image.image
            new_chibi._original_image = the_image.image
            new_chibi.costume = costume
            new_chibi.save()
            # card.chibis.remove(the_image)

        costume.save()

class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0055_auto_20180925_0752'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chibi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'cos/chibi'))),
                ('_original_image', models.ImageField(null=True, upload_to=magi.utils.uploadTiny(b'cos/chibi'))),
                ('costume', models.ForeignKey(related_name='owned_chibis', verbose_name='Costume', to='bang.Costume')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='costume',
            name='model_pkg',
            field=models.FileField(upload_to=magi.utils.uploadItem(b'cos/z'), null=True, verbose_name='Model'),
            preserve_default=True,
        ),
        migrations.RunPython(move_card_chibis),
        migrations.RemoveField(
            model_name='card',
            name='_cache_chibis_ids',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_chibis_last_update',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_chibis_paths',
        ),
        migrations.RemoveField(
            model_name='card',
            name='chibis',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AlterField(
            model_name='asset',
            name='i_band',
            field=models.PositiveIntegerField(help_text=b"Tagging a band is a shortcut to tagging all the members, so you don't need to tag the members when you tag a band.", null=True, verbose_name='Band', choices=[(0, b"Poppin'Party"), (1, b'Afterglow'), (2, b'Pastel*Palettes'), (3, b'Roselia'), (4, b'Hello, Happy World!')]),
            preserve_default=True,
        ),
    ]
