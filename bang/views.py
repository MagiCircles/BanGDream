# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.conf import settings as django_settings
from magi.utils import (
    redirectWhenNotAuthenticated,
    cuteFormFieldsForContext,
    CuteFormTransform,
    CuteFormType,
    get_one_object_or_404,
    staticImageURL,
)
from magi.item_model import get_image_url_from_path
from magi.views import settings as magi_settings
from bang.magicollections import CardCollection
from bang.forms import TeamBuilderForm
from bang import models

############################################################
# Default MagiCircles Views

def settings(request, context):
    magi_settings(request, context)
    cuteFormFieldsForContext({
        'd_extra-i_favorite_band': {
            'image_folder': 'band',
            'to_cuteform': 'value',
            'title': _('Band'),
            'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
        },
    }, context, context['forms']['preferences'])

############################################################
# Assets

def gallery(request, context):
    context['categories'] = [
        {
            'title': details['translation'],
            'url': u'/assets/{}/'.format(type),
            'icon': 'pictures',
            'image': staticImageURL(type, folder='gallery', extension='png'),
        } for i_type, (type, details) in enumerate(models.Asset.TYPES.items())
    ] + [
        {
            'icon': 'present',
            'title': _('Area items'),
            'url': '/areas/',
            'image': staticImageURL('area_items', folder='gallery', extension='png'),
        },
        {
            'icon': 'star',
            'title': _('Items'),
            'url': '/items/',
            'image': staticImageURL('items', folder='gallery', extension='png'),
        },
    ]

############################################################
# Team builder

SKILL_TYPE_TO_MAIN_VALUE = {
    '1': 'skill_percentage * (CASE i_skill_special WHEN 0 THEN {perfect_accuracy} WHEN 1 THEN {stamina_accuracy} ELSE 1 END)', # score up
    '2': '(CASE i_skill_special WHEN 1 THEN 0 ELSE skill_stamina END)', # life recovery
    '3': '5 - i_skill_note_type', # perfect lock, BAD = 1, GOOD = 2, GREAT = 3
}

def teambuilder(request, context):
    context['side_bar_no_padding'] = True
    context['learn_more_sentence'] = _('Learn more')
    context['js_files'] = ['teambuilder']

    if len(request.GET) > 0:
        form = TeamBuilderForm(request.GET, request=request)
        if form.is_valid():
            skill_type_main_value = SKILL_TYPE_TO_MAIN_VALUE.get(form.cleaned_data.get('i_skill_type', ''), '').format(
                perfect_accuracy=form.cleaned_data.get('perfect_accuracy', 0.8),
                stamina_accuracy=form.cleaned_data.get('stamina_accuracy', 0.8),
            )
            extra_select = {
                'overall_stats': u'CASE trained WHEN 1 THEN performance_trained_max + technique_trained_max + visual_trained_max ELSE performance_max + technique_max + visual_max END',
            }
            order_by = []
            if form.cleaned_data['i_band']:
                extra_select['is_correct_band'] = u'i_band = {}'.format(form.cleaned_data['i_band'])
                order_by.append('-is_correct_band')
            if form.cleaned_data['i_attribute']:
                extra_select['is_correct_attribute'] = u'i_attribute = {}'.format(form.cleaned_data['i_attribute'])
                order_by.append('-is_correct_attribute')
            if form.cleaned_data['i_skill_type']:
                extra_select['is_correct_skill'] = u'i_skill_type = {}'.format(form.cleaned_data['i_skill_type'])
                extra_select['skill_real_duration'] = u'skill_duration + ((IFNULL(skill_level, 1) - 1) * 0.5)'
                extra_select['skill_main_value'] = skill_type_main_value
                extra_select['skill_significant_value'] = u'({}) * ({})'.format(extra_select['skill_real_duration'], extra_select['skill_main_value'])
                order_by += ['-skill_significant_value', '-is_correct_skill']
            order_by += ['-overall_stats']
            queryset = form.Meta.model.objects.extra(select=extra_select).order_by(*order_by).select_related('card', 'card__member')
            queryset = form.filter_queryset(queryset, request.GET, request)

            # Only allow one of each member per team
            added_members = []
            team = []
            for cc in queryset:
                if request.user.is_staff:
                    cc.calculation_details = [
                        unicode(cc.card),
                        mark_safe(u'Ordering: <ol>{}</ol>'.format(''.join([
                            u'<li>{}</li>'.format(o.replace('-', '').replace('_', ' ').capitalize())
                            for o in order_by
                        ]))),
                    ]
                    if form.cleaned_data['i_skill_type']:
                        cc.calculation_details += [
                            u'Skill type: {}'.format(unicode(cc.card.t_skill_type)),
                            'Skill: {}'.format(cc.card.full_skill),
                            'Base skill duration: {}'.format(cc.card.skill_duration),
                            'Skill level: {}'.format(cc.skill_level or 1),
                            mark_safe(u'Real skill duration: {}<br><small class="text-muted">skill_duration + (skill_level - 1) * 0.5)</small>'.format(cc.skill_real_duration)),
                            mark_safe(u'Main value of skill: {}<br><small class="text-muted">{}</small>'.format(
                                cc.skill_main_value,
                                skill_type_main_value,
                            )),
                            mark_safe(u'Skill significant value: {}<br><small class="text-muted">real_skill_duration * main_value</small>'.format(cc.skill_significant_value),),
                        ]
                if cc.card.member_id in added_members:
                    continue
                team.append(cc)
                added_members.append(cc.card.member_id)
                if len(team) == int(form.cleaned_data.get('total_cards', 5) or 5):
                    break

            context['team'] = team
            context['no_container'] = True
        else:
            context['hide_side_bar'] = True
    else:
        form = TeamBuilderForm(request=request)
        context['hide_side_bar'] = True

    cuteFormFieldsForContext({
        'i_band': {
            'image_folder': 'band',
            'to_cuteform': 'value',
            'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
        },
        'i_attribute': {},
        'i_skill_type': {
            'to_cuteform': lambda k, v: CardCollection._skill_icons[k],
            'transform': CuteFormTransform.Flaticon,
        },
        'total_cards': {
            'type': CuteFormType.HTML,
        },
    }, context, form=form, prefix='#teambuilder-form ')

    context['filter_form'] = form

############################################################
# Tmp staff page to manage prizes assignment

import csv, datetime, urllib2
from dateutil.relativedelta import relativedelta
from magi import models as magi_models

PRIZE_ASSIGNMENT_SHEET = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRPhfuj6PeZYEr-8XacdzFqZ4BgyuT2UovNOb2B4DDF7uO3PTBRgl-JB_2VbSRdAXcQKkdYev1TP6kJ/pub?output=csv'
PRIZE_ASSIGNMENT_EDIT_URL = 'https://docs.google.com/spreadsheets/d/1WDqHoaP3tqNZnJb_vkFPLNL6RBwzBa7kSdkXEFuy1VE/edit#gid=1539095021'
BACKUP_PRIZES_ASSIGNMENT_SHEET = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQwGWoVQbplZpejj5DjJe92ifcOQ9bMUWYk7Wu-6AUMPYeOgKpxXTB_Xv_7TmoAjoOIqODdjwRrIBrR/pub?gid=741881890&single=true&output=csv'
BACKUP_PRIZES_ASSIGNMENT_EDIT_URL = 'https://docs.google.com/spreadsheets/d/1r0dhkhEOObc0Fm03TkSSDUejfTjpphCwl8o2rhkbCFs/edit?resourcekey#gid=741881890'

def generate_giveaway_discord_messages(request, context):
    context['backup_prizes'] = 'backup_prizes' in request.GET
    context['sheet_edit_url'] = BACKUP_PRIZES_ASSIGNMENT_EDIT_URL if context['backup_prizes'] else PRIZE_ASSIGNMENT_EDIT_URL

    discord_username = magi_models.StaffDetails.objects.get(owner=request.user).discord_username
    if not discord_username:
        context['no_discord_username'] = True
        return
    if discord_username.startswith('@'):
        discord_username = discord_username[1:]

    generated_messages = []

    cols_drawing = []
    if not context['backup_prizes']:
        cols_drawing_offsets = [ # or string value
            ('Type',  'Commissioned art'),
            ('Character',  0),
            ('Pose/style/scene',  1),
            ('Outfit',  2),
            ('Custom text',  3),
            ('Preferences (only if possible / not required)',  4),
        ]
    else:
        cols_drawing_offsets = [ # or string value
            ('Type',  'Custom drawing / fanart'),
            ('Character',  0),
            ('Pose/style/scene',  1),
            ('Pixel art', 2),
            ('With a background', 3),
            ('Outfit',  4),
            ('Custom text',  5),
        ]

    cols_edit = []
    cols_edit_offsets = [
        ('Commissioned graphic edit', 0),
        ('Size', 1),
        ('Description', 2),
        ('Custom text', 3),
    ]

    col_username = None
    col_entry = None
    col_title = []
    col_rank = None
    col_message = None
    col_event_title = None
    col_by = None
    col_shipped = None

    def get_prize_message(row, j, offsets, to_ping):
        if (col_by is not None and col_shipped is not None
            and (row[col_by].strip().lower() == 'asked'
                 or row[col_shipped].strip())):
            return None, None
        event_title = (row[col_event_title] if col_event_title is not None else 'Unknown').decode('utf-8')
        if context['backup_prizes']:
            event_title += u' (Backup prize)'
        generated = u''
        generated += to_ping + u'\n'
        generated += u'**Interested in making this prize?**' + u'\n'
        generated += u'1. Make sure your message in #🎨🖼🔗art_links is up to date (see <https://discordapp.com/channels/269845243648540673/502309402611810314/502311570483707904>)' + u'\n'
        generated += u'2. Reply here with:' + u'\n'
        recommended_date = datetime.date.today() + relativedelta(days=(2 if to_ping.startswith(u'@🖼') else 6))
        generated += u'　✩ When you think you can have it done (ex: {}{})'.format(
            recommended_date.strftime('%b %d'),
            { 1: 'st', 2: 'nd', 3: 'rd' }.get(recommended_date.day % 10 if recommended_date.day not in [11, 12, 13] else 0, 'th'),
        ) + u'\n'
        generated += u'　✩ Mention @{}'.format(discord_username) + u'\n'
        generated += u'3. Wait for confirmation.' + u'\n'
        generated += u'' + u'\n'
        generated += u'Thank you :heartfishy:' + u'\n'
        generated += u'' + u'\n'
        generated += u'Details of the prize to make:' + u'\n'
        for title, offset in offsets:
            if not isinstance(offset, int) or row[j + offset]:
                generated += u'✦  **{}:** {}'.format(title, row[j + offset].decode('utf-8') if isinstance(offset, int) else offset) + u'\n'
        if row[col_message]:
            generated += u'✦ **Message from the winner to the artist:**' + row[col_message].decode('utf-8') + u'\n'
        generated += u'' + u'\n'
        generated += u'Winner of the prize:' + u'\n'
        generated += u'✦ **Event:**' + event_title + u'\n'
        generated += u'✦ **Preferred name:**' + row[col_username] + u'\n'
        if col_entry is not None:
            generated += u'✦ **Winning entry:**' + row[col_entry] + u'\n'
        for j in col_title:
            if row[j]:
                generated += u'✦ **Winner\'s title**:' + row[j] + u'\n'
                break
        if col_rank is not None:
            generated += u'✦ **Rank**:' + row[col_rank] + u'\n'
        generated += u'' + u'\n'
        generated += u'✦ **Assigned to:** …' + u'\n'
        generated += u'✦ **Due date**: …' + u'\n'
        return event_title, generated

    csv_file = urllib2.urlopen(BACKUP_PRIZES_ASSIGNMENT_SHEET if context['backup_prizes'] else PRIZE_ASSIGNMENT_SHEET)
    csv_reader = csv.reader(csv_file)
    for i, row in enumerate(csv_reader):
        if i == 0: # Titles
            for j, col in enumerate(row):
                if col.strip() == 'Username':
                    col_username = j
                elif col.strip() == 'How do you prefer to be called?':
                    col_username = j
                elif col.strip() == 'How would you like to be called?':
                    col_username = j
                elif col.strip() == 'Entry':
                    col_entry = j
                elif col.strip() == 'Username / Winning category':
                    col_title.append(j)
                    col_username = j
                elif col.strip() in ['Winning category', 'Category']:
                    col_title.append(j)
                elif col.strip() in ['Rank', 'Your rank']:
                    col_rank = j
                elif col.strip() == 'Anything else to say?':
                    col_message = j
                elif col.strip() == 'Which character(s) or idolsona?':
                    cols_drawing.append(j)
                elif col.strip() == 'Which character(s)?':
                    cols_drawing.append(j)
                elif col.strip() == 'What kind of commission?':
                    cols_edit.append(j)
                elif col.endswith(' username') and col_username is None:
                    col_username = j
                elif col.strip() in ['Event', 'Awards', 'Giveaway']:
                    col_event_title = j
                elif col.strip().lower() == 'by':
                    col_by = j
                elif col.strip().lower() in ['shipped', 'received']:
                    col_shipped = j
        else:
            for j in cols_drawing:
                if row[j]:
                    event_title, message = get_prize_message(row, j, cols_drawing_offsets, u'@🎨 artists ')
                    if event_title and message:
                        generated_messages.append((event_title, message))
            for j in cols_edit:
                if row[j]:
                    event_title, message = get_prize_message(row, j, cols_edit_offsets, u'@🖼 designers ')
                    if event_title and message:
                        generated_messages.append((event_title, message))
    context['generated_messages'] = generated_messages
