# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bang', '0057_auto_20181128_0718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='areaitem',
            name='d_instruments',
        ),
        migrations.RemoveField(
            model_name='areaitem',
            name='depends_on_life',
        ),
        migrations.RemoveField(
            model_name='areaitem',
            name='flat',
        ),
        migrations.RemoveField(
            model_name='areaitem',
            name='i_band',
        ),
        migrations.RemoveField(
            model_name='areaitem',
            name='i_stat',
        ),
        migrations.RemoveField(
            model_name='areaitem',
            name='instrument',
        ),
        migrations.RemoveField(
            model_name='areaitem',
            name='value',
        ),
        migrations.RemoveField(
            model_name='eventparticipation',
            name='is_trial_master_completed',
        ),
        migrations.RemoveField(
            model_name='eventparticipation',
            name='is_trial_master_ex_completed',
        ),
        migrations.AddField(
            model_name='areaitem',
            name='about',
            field=models.TextField(null=True, verbose_name='About'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='areaitem',
            name='d_abouts',
            field=models.TextField(null=True, verbose_name='About'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='areaitem',
            name='i_boost_stat',
            field=models.PositiveIntegerField(null=True, verbose_name='Stat', choices=[(0, 'Performance'), (1, 'Technique'), (2, 'Visual')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='areaitem',
            name='i_instrument',
            field=models.PositiveIntegerField(null=True, verbose_name='Instrument', choices=[(0, 'Mic'), (1, 'Guitar'), (2, 'Bass'), (3, 'Drums'), (4, 'Other')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='areaitem',
            name='is_percent',
            field=models.BooleanField(default=True, verbose_name=b'Values are %?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='areaitem',
            name='lifes',
            field=models.CharField(help_text=b'Seperate with spaces in ascending order', max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='areaitem',
            name='max_level',
            field=models.PositiveIntegerField(default=5, verbose_name='Max Level'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='areaitem',
            name='values',
            field=models.CharField(help_text=b'Seperate with spaces in ascending order', max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='i_boost_stat',
            field=models.PositiveIntegerField(null=True, verbose_name='Boost stat', choices=[(0, 'Performance'), (1, 'Technique'), (2, 'Visual')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='is_ex_goal_master',
            field=models.NullBooleanField(verbose_name='EX Goal Master'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='is_goal_master',
            field=models.NullBooleanField(verbose_name='Goal Master'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='i_type',
            field=models.PositiveIntegerField(null=True, verbose_name='Type', choices=[(0, 'Main'), (1, 'Live Boost'), (2, 'Studio Ticket'), (3, 'Other')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='areaitem',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Location', to='bang.Area', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='areaitem',
            name='i_type',
            field=models.PositiveIntegerField(null=True, verbose_name='Area', choices=[(0, 'Studio'), (1, 'Poster'), (2, 'Counter'), (3, 'Mini Table'), (4, 'Magazine Rack'), (5, 'Entrance'), (6, 'Sign'), (7, 'Plaza'), (8, 'Garden'), (9, 'Specials Menu')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='areaitem',
            name='member',
            field=models.ForeignKey(related_name='area_items', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Member', to='bang.Member', help_text=b'Unless instrument, just choose member in affected band', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='i_type',
            field=models.PositiveIntegerField(default=0, verbose_name='Event type', choices=[(0, 'Normal'), (1, 'Challenge Live'), (2, 'VS Live'), (3, 'Live Goals'), (4, 'Mission Live')]),
            preserve_default=True,
        ),
    ]
