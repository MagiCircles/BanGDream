# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.utils.formats import dateformat
from web.magicollections import MagiCollection, AccountCollection as _AccountCollection, ActivityCollection as _ActivityCollection, BadgeCollection as _BadgeCollection, DonateCollection as _DonateCollection, UserCollection as _UserCollection
from web.utils import setSubField, CuteFormType, CuteFormTransform, FAVORITE_CHARACTERS_IMAGES, getMagiCollection
from web.default_settings import RAW_CONTEXT
from web.models import Activity
from bang.django_translated import t
from bang.utils import rarity_to_stars_images
from bang import models, forms

############################################################
# Default MagiCircles Collections

############################################################
# User Collection

class UserCollection(_UserCollection):
    class ItemView(_UserCollection.ItemView):
        def extra_context(self, context):
            super(UserCollection.ItemView, self).extra_context(context)
            accountCollection = getMagiCollection('account')
            if accountCollection:
                context['show_edit_button'] = (
                    accountCollection.item_view.show_edit_button
                    and accountCollection.edit_view.has_permissions(context['request'], context)
                )
                if accountCollection.edit_view.owner_only:
                    context['show_edit_button_owner_only'] = True
                for account in context['item'].all_accounts:
                    account.fields = accountCollection.to_fields(account)

############################################################
# Account Collection

class AccountCollection(_AccountCollection):
    form_class = forms.AccountForm

    filter_cuteform = {
        'member_id': {
            'to_cuteform': lambda k, v: FAVORITE_CHARACTERS_IMAGES[k],
            'extra_settings': {
	        'modal': 'true',
	        'modal-text': 'true',
            },
        },
    }

    def share_image(self, context, item):
        return 'screenshots/leaderboard.png'

    def get_queryset(self, queryset, parameters, request):
        return queryset.select_related('owner', 'owner__preferences')

    def to_fields(self, item, *args, **kwargs):
        return super(AccountCollection, self).to_fields(item, *args, icons={
            'creation': 'date',
            'start_date': 'date',
            'level': 'max-level',
        }, **kwargs)

    class ListView(_AccountCollection.ListView):
        show_edit_button = False
        filter_form = forms.FilterAccounts
        default_ordering = '-level'

    class AddView(_AccountCollection.AddView):
        back_to_list_button = False

        def redirect_after_add(self, request, item, ajax):
            return '/cards/?get_started'

############################################################
# Badge Collection

class BadgeCollection(_BadgeCollection):
    enabled = True

############################################################
# Donate Collection

class DonateCollection(_DonateCollection):
    enabled = True

############################################################
# Activity Collection

class ActivityCollection(_ActivityCollection):
    enabled = False
    class ListView(_ActivityCollection.ListView):
        before_template = 'include/index'

Activity.collection_name = 'news'

class NewsCollection(_ActivityCollection):
    plural_name = 'news'
    reportable = False
    queryset = Activity.objects.all()

    class ListView(_ActivityCollection.ListView):
        enabled = False

    class ItemView(_ActivityCollection.ItemView):
        template = 'activityItem'

    class AddView(_ActivityCollection.AddView):
        staff_required = True

############################################################
############################################################
############################################################

############################################################
# Member Collection

class MemberCollection(MagiCollection):
    queryset = models.Member.objects.all()
    title = _('Member')
    plural_title = _('Members')
    icon = 'idolized'

    reportable = False

    form_class = forms.MemberForm

    def share_image(self, context, item):
        return 'screenshots/members.png'

    def to_fields(self, item, *args, **kwargs):
        fields = super(MemberCollection, self).to_fields(item, *args, icons={
            'name': 'id',
            'japanese_name': 'id',
            'band': 'users',
            'school': 'max-bond',
            'school_year': 'max-bond',
            'CV': 'profile',
            'romaji_CV': 'profile',
            'birthday': 'event',
            'food_likes': 'heart',
            'food_dislikes': 'heart-empty',
            'hobbies': 'star',
            'description': 'id',
            'cards': 'album',
            'fans': 'heart',
        }, images={
            'astrological_sign': '{}img/i_astrological_sign/{}.png'.format(RAW_CONTEXT['static_url'], item.i_astrological_sign),
        }, **kwargs)
        if 'square_image' in fields:
            del(fields['square_image'])
        setSubField(fields, 'birthday', key='value', value=lambda f: dateformat.format(item.birthday, "F d"))
        setSubField(fields, 'band', key='type', value=lambda f: 'image_link')
        setSubField(fields, 'band', key='link', value=lambda f: u'/members/?i_band={}'.format(item.i_band))
        setSubField(fields, 'band', key='ajax_link', value=lambda f: u'/ajax/members/?i_band={}&ajax_modal_only'.format(item.i_band))
        setSubField(fields, 'band', key='link_text', value=lambda f: item.band)
        setSubField(fields, 'band', key='value', value=lambda f: '{}img/band/{}.png'.format(RAW_CONTEXT['static_url'], item.band))
        setSubField(fields, 'description', key='type', value='long_text')
        if get_language() == 'ja':
            setSubField(fields, 'CV', key='verbose_name', value=_('CV'))
            if 'romaji_CV' in fields:
                del(fields['romaji_CV'])
        if 'description' in fields:
            fields['source'] = {
                'verbose_name': _('Source'),
                'link_text': 'BanGDreaming Tumblr',
                'type': 'link',
                'value': 'https://bangdreaming.tumblr.com/chara',
            }
        return fields

    filter_cuteform = {
        'i_band': {
            'image_folder': 'band',
            'to_cuteform': 'value',
            'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
        },
        'i_school_year': {
            'type': CuteFormType.HTML,
        },
        'i_astrological_sign': {},
    }

    class ItemView(MagiCollection.ItemView):
        template = 'default'

    class ListView(MagiCollection.ListView):
        filter_form = forms.MemberFilterForm
        default_ordering = '-_cache_total_fans'

    class AddView(MagiCollection.AddView):
        staff_required = True
        multipart = True

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True

############################################################
# Card Collection

class CardCollection(MagiCollection):
    queryset = models.Card.objects.all()
    title = _('Card')
    plural_title = _('Cards')
    icon = 'deck'
    collectible = models.CollectibleCard

    form_class = forms.CardForm
    reportable = False

    filter_cuteform = {
        'member_id': {
            'to_cuteform': lambda k, v: FAVORITE_CHARACTERS_IMAGES[k],
            'extra_settings': {
	        'modal': 'true',
	        'modal-text': 'true',
            },
        },
        'i_rarity': {
            'type': CuteFormType.HTML,
            'to_cuteform': lambda k, v: rarity_to_stars_images(k),
        },
        'i_attribute': {},
        'trainable': {
            'type': CuteFormType.OnlyNone,
        },
        'i_skill_type': {
            'to_cuteform': lambda k, v: models.SKILL_ICONS[k],
            'transform': CuteFormTransform.Flaticon,
        },
        'member_band': {
            'image_folder': 'band',
            'to_cuteform': 'value',
            'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
        },
    }

    def share_image(self, context, item):
        return 'screenshots/cards.png'

    def to_fields(self, item, only_fields=None, in_list=False):
        # Used in ordering
        if in_list:
            fields = super(CardCollection, self).to_fields(item, icons={
                '_cache_member_name': 'id',
                '_cache_member_japanese_name': 'id',
                'rarity': 'star',
                'performance_max': 'skill',
                'performance_trained_max': 'skill',
                'technique_max': 'skill',
                'technique_trained_max': 'skill',
                'visual_max': 'skill',
                'visual_trained_max': 'skill',
            }, images={
                'attribute': u'{static_url}img/i_attribute/{value}.png'.format(
                    static_url=RAW_CONTEXT['static_url'],
                    value=item.i_attribute,
                ),
            }, only_fields=only_fields, in_list=in_list)
            setSubField(fields, 'rarity', key='type', value='html')
            setSubField(fields, 'rarity', key='value', value=lambda f: rarity_to_stars_images(item.i_rarity))
            if '_overall_max' in only_fields:
                fields['overall_max'] = {
                    'verbose_name': string_concat(_('Overall'), ' (', _('Maximum'), ')'),
                    'value': item._overall_max,
                    'type': 'text',
                    'icon': 'center',
                }
            if '_overall_trained_max' in only_fields:
                fields['overall_trained_max'] = {
                    'verbose_name': string_concat(_('Overall'), ' (', _('Trained'), ', ', _('Maximum'), ')'),
                    'value': item._overall_trained_max,
                    'type': 'text',
                    'icon': 'center',
                }
            return fields
        # Used in cards description
        final_fields = OrderedDict([(field, info) for field, info in [
            # field name: (icon, verbose name, extra field info)
            ('id', ('id', _('ID'), None)),
            ('member', ('idolized', _('Member'), None)),
            ('name', ('id', _('Title'), {
                'type': 'title_text',
                'title': item.name,
                'value': item.japanese_name,
            } if (item.name or item.japanese_name) and get_language() != 'ja' else {})),
            ('skill_name', ('skill', _('Skill name'), {
                'type': 'title_text',
                'title': item.skill_name,
                'value': item.japanese_skill_name,
            } if (item.skill_name or item.japanese_skill_name) and get_language() != 'ja' else {})),
            ('skill', (models.SKILL_ICONS[item.i_skill_type], _('Skill'), {
                'type': 'title_text',
                'title': item.skill_type,
            })),
            ('japanese_skill', (models.SKILL_ICONS[item.i_skill_type], string_concat(_('Skill'), ' (', t['Japanese'], ')'), {
                'type': 'title_text',
                'title': item.japanese_skill_type,
            })),
            ('image', ('id', _('Icon'), {
                'type': 'image',
                'value': item.image_url,
            })),
            ('image_trained', ('id', string_concat(_('Icon'), ' (', _('Trained'), ')'), None)),
            ('art', ('link', _('Art'), None)),
            ('art_trained', ('link', string_concat(_('Art'), ' (', _('Trained'), ')'), None)),
            ('transparent', ('link', _('Transparent'), None)),
            ('transparent_trained', ('link', string_concat(_('Transparent'), ' (', _('Trained'), ')'), None)),
        ] if item.trainable or '_trained' not in field])
        if get_language() == 'ja':
            if 'skill' in final_fields:
                del(final_fields['skill'])
            icon, localized, field_info = final_fields['japanese_skill']
            final_fields['japanese_skill'] = (icon, _('Skill'), field_info)
        fields = super(CardCollection, self).to_fields(item, to_dict=True, only_fields=final_fields, in_list=in_list)
        new_fields = OrderedDict()
        for field, (icon, verbose_name, field_info) in final_fields.items():
            field_info = field_info if field_info else {}
            field_info.update({
                'verbose_name': verbose_name,
                'icon': icon,
            })
            if field in fields:
                new_fields[field] = fields[field]
                new_fields[field].update(field_info)
            else:
                if only_fields and field not in only_fields:
                    continue
                new_fields[field] = {
                    'type': 'text',
                }
                new_fields[field].update(field_info)
                if 'value' not in new_fields[field]:
                    try:
                        new_fields[field]['value'] = getattr(item, field)
                    except AttributeError:
                        pass
                    if not new_fields[field]['value']:
                        del(new_fields[field])
        return new_fields

    class ItemView(MagiCollection.ItemView):
        template = 'default'
        top_illustration = 'items/cardItem'
        ajax_callback = 'loadCard'

    class ListView(MagiCollection.ListView):
        per_line = 2
        filter_form = forms.CardFilterForm
        default_ordering = '-id'

        def get_queryset(self, queryset, parameters, request):
            if request.GET.get('ordering', None) in ['_overall_max', '_overall_trained_max']:
                queryset = queryset.extra(select={
                    '_overall_max': 'performance_max + technique_max + visual_max',
                    '_overall_trained_max': 'performance_trained_max + technique_trained_max + visual_trained_max',
                })
            return queryset

    class AddView(MagiCollection.AddView):
        staff_required = True
        multipart = True

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True
