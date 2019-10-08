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
