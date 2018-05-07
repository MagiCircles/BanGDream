from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.conf import settings as django_settings
from magi.utils import getGlobalContext, redirectWhenNotAuthenticated, cuteFormFieldsForContext, CuteFormTransform, get_one_object_or_404
from magi.item_model import get_image_url_from_path
from magi.views import indexExtraContext
from bang.magicollections import CardCollection
from bang.forms import TeamBuilderForm
from bang.models import Card

LIVE2D_JS_FILES = [
    "l2d/zip",
    "l2d/zip-ext",
    "l2d/z-worker.combo",
    "l2d/ZipLoader",
    "l2d/live2d.min",
    "l2d/Live2DFramework",
    "l2d/MatrixStack",
    "l2d/ModelSettingJson",
    "l2d/LAppModel",
    "l2d/DirectorLite",
]

def live2d_ajax(request, pk):
    context = getGlobalContext(request)
    queryset = Card.objects.filter(id=pk, live2d_model_pkg__isnull=False)
    the_card = get_one_object_or_404(queryset)

    context['item'] = the_card
    context['package_url'] = get_image_url_from_path(the_card.live2d_model_pkg)
    context['js_files'] = LIVE2D_JS_FILES

    return render(request, 'pages/live2dajax.html', context)

def live2d(request, pk, slug=None):
    context = getGlobalContext(request)
    queryset = Card.objects.filter(id=pk, live2d_model_pkg__isnull=False)
    the_card = get_one_object_or_404(queryset)

    context['page_title'] = u"{}: {}".format(_('Live2D'), unicode(the_card))
    context['item'] = the_card
    context['package_url'] = get_image_url_from_path(the_card.live2d_model_pkg)
    context['js_files'] = LIVE2D_JS_FILES

    return render(request, 'pages/live2dviewer.html', context)

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
