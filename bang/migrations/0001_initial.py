# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('level', models.PositiveIntegerField(null=True, verbose_name='Level')),
                ('owner', models.ForeignKey(related_name='accounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.PositiveIntegerField(unique=True, serialize=False, verbose_name='ID', primary_key=True, db_index=True)),
                ('i_rarity', models.PositiveIntegerField(verbose_name='Rarity', choices=[(1, '\u2605'), (2, '\u2605\u2605'), (3, '\u2605\u2605\u2605'), (4, '\u2605\u2605\u2605\u2605')])),
                ('i_attribute', models.PositiveIntegerField(verbose_name='Attribute', choices=[(1, 'Power'), (2, 'Cool'), (3, 'Pure'), (4, 'Happy')])),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'c'), verbose_name='Icon')),
                ('image_trained', models.ImageField(upload_to=magi.utils.uploadItem(b'c/a'), verbose_name='Icon (Trained)')),
                ('art', models.ImageField(upload_to=magi.utils.uploadItem(b'c/art'), verbose_name='Art')),
                ('art_trained', models.ImageField(upload_to=magi.utils.uploadItem(b'c/art/a'), verbose_name='Art (Trained)')),
                ('transparent', models.ImageField(upload_to=magi.utils.uploadItem(b'c/transparent'), verbose_name='Transparent')),
                ('transparent_trained', models.ImageField(upload_to=magi.utils.uploadItem(b'c/transparent/a'), verbose_name='Transparent (Trained)')),
                ('skill_name', models.CharField(max_length=100, null=True, verbose_name=b'Skill name')),
                ('japanese_skill_name', models.CharField(max_length=100, null=True, verbose_name=b'Skill name (Japanese)')),
                ('i_skill_type', models.PositiveIntegerField(verbose_name='Skill', choices=[(1, 'Score Up'), (2, 'Life Recovery'), (3, 'Perfect Lock')])),
                ('skill_details', models.CharField(max_length=200, null=True, verbose_name='Skill')),
                ('performance_min', models.PositiveIntegerField(default=0, verbose_name='Performance (Minimum)')),
                ('performance_max', models.PositiveIntegerField(default=0, verbose_name='Performance (Maximum)')),
                ('performance_trained_max', models.PositiveIntegerField(default=0, verbose_name='Performance (Trained, Maximum)')),
                ('technique_min', models.PositiveIntegerField(default=0, verbose_name='Technique (Minimum)')),
                ('technique_max', models.PositiveIntegerField(default=0, verbose_name='Technique (Maximum)')),
                ('technique_trained_max', models.PositiveIntegerField(default=0, verbose_name='Technique (Trained, Maximum)')),
                ('visual_min', models.PositiveIntegerField(default=0, verbose_name='Visual (Minimum)')),
                ('visual_max', models.PositiveIntegerField(default=0, verbose_name='Visual (Maximum)')),
                ('visual_trained_max', models.PositiveIntegerField(default=0, verbose_name='Visual (Trained, Maximum)')),
                ('_cache_member_last_update', models.DateTimeField(null=True)),
                ('_cache_member_name', models.CharField(max_length=100, null=True)),
                ('_cache_member_japanese_name', models.CharField(max_length=100, null=True)),
                ('_cache_member_image', models.ImageField(null=True, upload_to=magi.utils.uploadItem(b'member'), blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name (romaji)')),
                ('japanese_name', models.CharField(max_length=100, null=True, verbose_name='Name (Japanese)')),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), verbose_name='Image')),
                ('square_image', models.ImageField(upload_to=magi.utils.uploadItem(b'i/m'), verbose_name='Image')),
                ('i_band', models.PositiveIntegerField(verbose_name='Band', choices=[(0, b"poppin' party"), (1, b'afterglow'), (2, b'pastel*palettes'), (3, b'roselia'), (4, b'hello, happy world!')])),
                ('school', models.CharField(max_length=100, null=True, verbose_name='School')),
                ('i_school_year', models.PositiveIntegerField(null=True, verbose_name='School Year', choices=[(0, 'First'), (1, 'Second'), (2, 'Third')])),
                ('romaji_CV', models.CharField(help_text=b'In romaji.', max_length=100, null=True, verbose_name='CV')),
                ('CV', models.CharField(help_text=b'In Japanese characters.', max_length=100, null=True, verbose_name='CV (Japanese)')),
                ('birthday', models.DateField(help_text=b'The year is not used, so write whatever', null=True, verbose_name='Birthday')),
                ('food_likes', models.CharField(max_length=100, null=True, verbose_name='Liked food')),
                ('food_dislikes', models.CharField(max_length=100, null=True, verbose_name='Disliked food')),
                ('i_astrological_sign', models.PositiveIntegerField(null=True, verbose_name='Astrological Sign', choices=[(0, 'Leo'), (1, 'Aries'), (2, 'Libra'), (3, 'Virgo'), (4, 'Scorpio'), (5, 'Capricorn'), (6, 'Pisces'), (7, 'Gemini'), (8, 'Cancer'), (9, 'Sagittarius'), (10, 'Aquarius'), (11, 'Taurus')])),
                ('hobbies', models.CharField(max_length=100, null=True, verbose_name='Hobbies')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('_cache_totals_last_update', models.DateTimeField(null=True)),
                ('_cache_total_fans', models.PositiveIntegerField(null=True)),
                ('_cache_total_cards', models.PositiveIntegerField(null=True)),
                ('owner', models.ForeignKey(related_name='added_members', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='card',
            name='member',
            field=models.ForeignKey(related_name='cards', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Member', to='bang.Member', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='owner',
            field=models.ForeignKey(related_name='added_cards', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
