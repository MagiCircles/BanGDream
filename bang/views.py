from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.conf import settings as django_settings
from magi.utils import getGlobalContext, redirectWhenNotAuthenticated, cuteFormFieldsForContext, CuteFormTransform
from magi.views import indexExtraContext
from bang.magicollections import CardCollection
from bang.forms import TeamBuilderForm

def discord(request):
    return redirect('https://discord.gg/8wrXKX3')

def twitter(request):
    return redirect('https://twitter.com/bandoriparty')

def teambuilder(request):
    context = getGlobalContext(request)

    redirectWhenNotAuthenticated(request, context, next_title=_('Team builder'))
    context['page_title'] = _('Team builder')
    context['side_bar_no_padding'] = True

    if len(request.GET) > 0:
        form = TeamBuilderForm(request.GET, request=request)
        if form.is_valid():
            extra_select = {
                'is_correct_band': u'i_band = {}'.format(form.cleaned_data['i_band']),
                'is_correct_attribute': u'i_attribute = {}'.format(form.cleaned_data['i_attribute']),
                'overall_stats': u'CASE trained WHEN 1 THEN performance_trained_max + technique_trained_max + visual_trained_max ELSE performance_max + technique_max + visual_max END',
            }
            order_by = [
                '-is_correct_band',
                '-is_correct_attribute',
            ]
            if form.cleaned_data['i_skill_type']:
                extra_select['is_correct_skill'] = u'i_skill_type = {}'.format(form.cleaned_data['i_skill_type'])
                order_by.append('is_correct_skill')
            order_by += ['-overall_stats']
            queryset = form.Meta.model.objects.extra(select=extra_select).order_by(*order_by).select_related('card', 'card__member')
            queryset = form.filter_queryset(queryset, request.GET, request)
            context['team'] = queryset[:5]
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
    }, context, form=form, prefix='#teambuilder-form ')

    context['filter_form'] = form
    return render(request, 'pages/teambuilder.html', context)
