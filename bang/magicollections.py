# -*- coding: utf-8 -*-
import math, simplejson, random
from itertools import chain
from collections import OrderedDict
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.utils.formats import dateformat
from django.utils.safestring import mark_safe
from django.db.models import Prefetch, Q
from django.db.models.fields import BLANK_CHOICE_DASH
from magi.magicollections import MagiCollection, AccountCollection as _AccountCollection, ActivityCollection as _ActivityCollection, BadgeCollection as _BadgeCollection, DonateCollection as _DonateCollection, UserCollection as _UserCollection, StaffConfigurationCollection as _StaffConfigurationCollection
from magi.utils import setSubField, CuteFormType, CuteFormTransform, FAVORITE_CHARACTERS_IMAGES, getMagiCollection, torfc2822, custom_item_template, staticImageURL, justReturn, jsv
from magi.default_settings import RAW_CONTEXT
from magi.item_model import i_choices
from magi.models import Activity, Notification
from bang.constants import LIVE2D_JS_FILES
from bang import settings
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
            if context['item'].id == context['request'].user.id:
                context['hashtags'] = context['hashtags'] + ['MyBanpaCollection']
            if get_language() == 'en':
                context['share_sentence'] = u'Hey, look! I\'m on ✭Bandori Party✭! Follow me ♥︎'

    class ListView(_UserCollection.ListView):
        filter_form = forms.FilterUsers

############################################################
# Account Collection

class AccountCollection(_AccountCollection):
    form_class = forms.AccountForm
    navbar_link_list = 'community'

    _colors_images = [_c[0] for _c in settings.USER_COLORS]
    _version_images = [_c['image'] for _c in models.Account.VERSIONS.values()]
    _play_with_icons = [_c['icon'] for _c in models.Account.PLAY_WITH.values()]
    filter_cuteform = {
        'member': {
            'to_cuteform': lambda k, v: FAVORITE_CHARACTERS_IMAGES[k],
            'title': _('Member'),
            'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
        },
        'i_color': {
            'to_cuteform': lambda k, v: AccountCollection._colors_images.index(k) + 1,
            'image_folder': 'i_attribute',
            'transform': CuteFormTransform.ImagePath,
        },
        'has_friend_id': {
            'type': CuteFormType.OnlyNone,
        },
        'center': {
            'to_cuteform': lambda k, v: v.image_url,
            'title': _('Center'),
            'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
        },
        'i_version': {
            'to_cuteform': lambda k, v: AccountCollection._version_images[k],
            'image_folder': 'language',
            'transform': CuteFormTransform.ImagePath,
        },
        'i_play_with': {
            'to_cuteform': lambda k, v: AccountCollection._play_with_icons[k],
            'transform': CuteFormTransform.FlaticonWithText,
        },
        'i_os': {
            'to_cuteform': lambda k, v: models.Account.OS_CHOICES[k],
            'transform': CuteFormTransform.FlaticonWithText,
        },
    }

    def to_fields(self, view, item, exclude_fields=None, *args, **kwargs):
        if exclude_fields is None: exclude_fields = []
        exclude_fields.append('owner')
        fields = super(AccountCollection, self).to_fields(view, item, *args, icons={
            'play_with': item.play_with_icon,
            'os': item.os_icon,
            'device': item.os_icon or 'id',
        }, images={
            'version': item.version_image_url,
            'stargems_bought': staticImageURL(u'stargems_bought.png'),
        }, exclude_fields=exclude_fields, **kwargs)
        setSubField(fields, 'stargems_bought', key='verbose_name', value=_('Total {item} bought').format(item=_('Star gems').lower()))
        setSubField(fields, 'stargems_bought', key='type', value='text_annotation')
        spent_yen = int(item.stargems_bought * django_settings.PRICE_PER_STARGEM) if item.stargems_bought else 0
        spent_dollars = int(spent_yen * django_settings.YEN_TO_USD)
        setSubField(fields, 'stargems_bought', key='annotation', value=_(u'~{}円 spent (~${})').format(spent_yen, spent_dollars))
        return fields

    def get_profile_account_tabs(self, request, context, *args, **kwargs):
        tabs = super(AccountCollection, self).get_profile_account_tabs(request, context, *args, **kwargs)
        for collection_name, collection in context['collectible_collections']['account'].items():
            if collection_name in ['collectibleitem', 'collectibleareaitem']:
                tabs[collection_name]['callback'] = 'function loadAccountComingSoon(tab_name, user_id, account_id, onDone) { onDone(\'<div class="alert alert-info text-center"><i class="flaticon-idolized"></i> \' + gettext(\'Coming soon\') + \' <i class="flaticon-idolized"></i></div>\'); }'
        return tabs

    def share_image(self, context, item):
        return 'screenshots/leaderboard.png'

    class ListView(_AccountCollection.ListView):
        filter_form = forms.FilterAccounts
        default_ordering = '-level'

        def buttons_per_item(self, request, context, item):
            buttons = super(AccountCollection.ListView, self).buttons_per_item(request, context, item)
            buttons['version'] = {
                'show': True, 'has_permissions': True, 'image': u'language/{}'.format(item.version_image),
                'title': item.t_version, 'url': u'{}?i_version={}'.format(
                    self.collection.get_list_url(),
                    item.i_version,
                ), 'classes': [],
            }
            return buttons

    class AddView(_AccountCollection.AddView):
        back_to_list_button = False
        simpler_form = forms.AddAccountForm

        def redirect_after_add(self, request, item, ajax):
            if not ajax:
                return '/cards/?get_started&add_to_collectiblecard={account_id}&view=icons&version={account_version}&ordering=i_rarity&reverse_order=on'.format(
                    account_id=item.id,
                    account_version=item.version,
                )
            return super(AccountCollection.AddView, self).redirect_after_add(request, item, ajax)

############################################################
# Badge Collection

class BadgeCollection(_BadgeCollection):
    enabled = True

############################################################
# Staff Configuration Collection

class StaffConfigurationCollection(_StaffConfigurationCollection):
    enabled = True

############################################################
# Donate Collection

class DonateCollection(_DonateCollection):
    enabled = True
    navbar_link_list = 'community'
    navbar_link_list_divider_after = True

############################################################
# Activity Collection

class ActivityCollection(_ActivityCollection):
    navbar_link = True
    navbar_link_list = 'community'

    class ListView(_ActivityCollection.ListView):
        before_template = 'include/index'

        def extra_context(self, context):
            super(ActivityCollection.ListView, self).extra_context(context)

            # Homepage settings
            if 'shortcut_url' in context and context['shortcut_url'] == '':

                context['full_width'] = True
                context['page_title'] = None

                # Staff cards preview
                if (context['request'].user.is_authenticated()
                    and context['request'].user.hasPermission('manage_main_items')
                    and 'preview' in context['request'].GET):
                    context['random_card'] = {
                        'art_url': context['request'].GET['preview'],
                    }
                # 1 chance out of 5 to get a random card of 1 of your favorite characters
                elif (context['request'].user.is_authenticated()
                      and context['request'].user.preferences.favorite_characters
                      and random.randint(0, 5) == 5):
                    try:
                        character_id = random.choice(context['request'].user.preferences.favorite_characters)
                        card = (models.Card.objects.filter(
                            member_id=character_id,
                        ).exclude(Q(art__isnull=True) | Q(art='')).exclude(i_rarity=1).exclude(
                            show_art_on_homepage=False, show_trained_art_on_homepage=False,
                        ).order_by('?'))[0]
                    except IndexError:
                        card = None
                    if card:
                        context['random_card'] = {
                            'art_url': random.choice([u for u, s in [
                                (card.art_url, card.show_art_on_homepage),
                                (card.art_trained_url, card.show_trained_art_on_homepage),
                            ] if u and s]),
                            'item_url': card.item_url,
                        }
                # Random from the last 20 released cards
                elif django_settings.HOMEPAGE_CARDS:
                    context['random_card'] = random.choice(django_settings.HOMEPAGE_CARDS)
                # If no random_card was available
                if 'random_card' not in context:
                    context['random_card'] = {
                        'art_url': '//i.bandori.party/u/c/art/838Kasumi-Toyama-Happy-Colorful-Poppin-WV6jFP.png',
                    }

############################################################
############################################################
############################################################

############################################################
# Member Collection

MEMBERS_ICONS = {
    'name': 'id',
    'japanese_name': 'id',
    'band': 'users',
    'school': 'id',
    'school_year': 'id',
    'CV': 'profile',
    'romaji_CV': 'profile',
    'birthday': 'event',
    'food_like': 'heart',
    'food_dislike': 'heart-empty',
    'instrument': 'star',
    'hobbies': 'star-empty',
    'description': 'id',
    'cards': 'album',
    'fans': 'heart',
    'costumes': 'profile',
}

class MemberCollection(MagiCollection):
    queryset = models.Member.objects.all()
    title = _('Member')
    plural_title = _('Members')
    navbar_link_title = _('Characters')
    icon = 'idolized'
    navbar_link_list = 'bangdream'
    translated_fields = ('name',  'school', 'food_like', 'food_dislike', 'instrument', 'hobbies', 'description', )

    reportable = False
    blockable = False

    form_class = forms.MemberForm

    def share_image(self, context, item):
        return 'screenshots/members.png'

    def to_fields(self, view, item, exclude_fields=None, *args, **kwargs):
        if exclude_fields is None: exclude_fields = []
        exclude_fields.append('d_names')
        fields = super(MemberCollection, self).to_fields(view, item, *args, icons=MEMBERS_ICONS, images={
            'astrological_sign': '{}img/i_astrological_sign/{}.png'.format(RAW_CONTEXT['static_url'], item.i_astrological_sign),
        }, exclude_fields=exclude_fields, **kwargs)
        if 'square_image' in fields:
            del(fields['square_image'])
        setSubField(fields, 'birthday', key='type', value='text')
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
        if 'description' in fields and get_language() == 'en':
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
            'title': _('Band'),
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

    class ListView(MagiCollection.ListView):
        item_template = custom_item_template
        filter_form = forms.MemberFilterForm
        default_ordering = 'id'

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']
        multipart = True

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']
        multipart = True

############################################################
# Favorite Card Collection

def to_FavoriteCardCollection(cls):
    class _FavoriteCardCollection(cls):
        @property
        def title(self):
            return _('Favorite {thing}').format(thing=_('Card').lower())

        @property
        def plural_title(self):
            return _('Favorite {things}').format(things=_('Cards').lower())

        class ListView(cls.ListView):
            item_template = 'cardItem'
            per_line = 2
            default_ordering = '-id'
            ajax_pagination_callback = 'loadCardInList'
            show_item_buttons = True

        class AddView(cls.AddView):
            unique_per_owner = True
            quick_add_to_collection = justReturn(True)

        class EditView(cls.EditView):
            def extra_context(self, context):
                edit_form = context.get('forms', {}).get('edit_favoritecard', None)
                if edit_form is not None:
                    edit_form.beforeform = mark_safe(u'<div class="hidden">')
                    edit_form.belowform = mark_safe(u'</div>')

    return _FavoriteCardCollection

############################################################
# Collectible Card Collection

COLLECTIBLE_CARDS_ICONS = {
    'trained': 'idolized',
    'max_leveled': 'max-level',
    'first_episode': 'play',
    'memorial_episode': 'play',
    'skill_level': 'skill',
}

COLLECTIBLE_CARDS_ORDER = [
    'card', 'trained', 'max_leveled',
    'performance', 'technique', 'visual', 'overall',
    'first_episode', 'memorial_episode', 'skill_level',
]

def to_CollectibleCardCollection(cls):
    class _CollectibleCardCollection(cls):
        title = _('Card')
        plural_title = _('Cards')
        form_class = forms.to_CollectibleCardForm(cls)

        filter_cuteform = CardCollection.filter_cuteform.copy()
        _f = filter_cuteform.update({
            'max_leveled': {
                'type': CuteFormType.YesNo,
            },
            'first_episode': {
                'type': CuteFormType.YesNo,
            },
            'memorial_episode': {
                'type': CuteFormType.YesNo,
            },
        })

        def to_fields(self, view, item, order=None, exclude_fields=None, extra_fields=None, *args, **kwargs):
            if exclude_fields is None: exclude_fields = []
            if extra_fields is None: extra_fields = []
            if order is None:
                order = COLLECTIBLE_CARDS_ORDER
            exclude_fields.append('prefer_untrained')
            if item.card.i_rarity not in models.Card.TRAINABLE_RARITIES:
                exclude_fields.append('trained')
            # Add stats
            stats = dict(item.card.stats_percent)
            stats = stats['trained_max'] if item.trained else stats['max']
            extra_fields += [
                (stat, {
                    'verbose_name': verbose_name,
                    'verbose_name_subtitle': _(u'Level {level}').format(
                        level=item.card.max_level_trained if item.trained else item.card.max_level,
                    ).replace(' ', u'\u00A0'),
                    'value': value,
                    'type': 'text',
                    'icon': 'skill' if stat != 'overall' else 'center',
                })
                for stat, verbose_name, value, _max, _percentage in stats
            ]
            # Add skill
            if item.card.skill_type:
                extra_fields.append(('skill', {
                    'title': mark_safe(u'{} <span class="text-muted">({})</span>'.format(
                        item.card.t_skill_type.replace(' ', u'\u00A0'),
                        item.card.t_side_skill_type.replace(' ', u'\u00A0')))
                    if item.card.i_side_skill_type else item.card.t_skill_type,
                    'verbose_name': _('Skill'),
                    'icon': item.card.skill_icon,
                    'value': item.full_skill,
                    'type': 'title_text',
                }))

            fields = super(_CollectibleCardCollection, self).to_fields(view, item, *args, icons=COLLECTIBLE_CARDS_ICONS, order=order, exclude_fields=exclude_fields, extra_fields=extra_fields, **kwargs)
            setSubField(fields, 'card', key='value', value=u'#{}'.format(item.card.id))
            setSubField(fields, 'first_episode', key='verbose_name', value=_('{nth} episode').format(nth=_('1st')))
            return fields

        class ListView(cls.ListView):
            col_break = 'xs'
            default_ordering = '-card__i_rarity,-trained,-card__release_date'
            filter_form = forms.to_CollectibleCardFilterForm(cls)

        class AddView(cls.AddView):
            unique_per_owner = True
            ajax_callback = 'loadCollecticleCardForm'

            def quick_add_to_collection(self, request):
                return request.GET.get('view') == 'icons'

            add_to_collection_variables = cls.AddView.add_to_collection_variables + [
                'i_rarity',
            ]

        class EditView(cls.EditView):
            ajax_callback = 'loadCollecticleCardForm'

    return _CollectibleCardCollection

############################################################
# Card Collection

CARD_CUTEFORM = {
    'member': {
        'to_cuteform': lambda k, v: FAVORITE_CHARACTERS_IMAGES[k],
        'title': _('Member'),
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
        'to_cuteform': lambda k, v: CardCollection._skill_icons[k],
        'transform': CuteFormTransform.Flaticon,
    },
    'member_band': {
        'image_folder': 'band',
        'to_cuteform': 'value',
        'title': _('Band'),
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
    'version': {
        'to_cuteform': lambda k, v: CardCollection._version_images[k],
        'image_folder': 'language',
        'transform': CuteFormTransform.ImagePath,
    },
    'origin': {
        'transform': CuteFormTransform.Flaticon,
        'to_cuteform': lambda k, v: CardCollection._origin_to_cuteform[k],
    },
    'is_limited': {
        'type': CuteFormType.YesNo,
    },
}

CARDS_STATS_FIELDS = [
    u'{}{}'.format(_st, _sf) for _st in [
        'performance', 'technique', 'visual', 'overall',
    ] for _sf in [
        '_min', '_max', '_trained_max',
    ]
]

CARDS_ICONS = { _st: 'skill' for _st in CARDS_STATS_FIELDS }
CARDS_ICONS.update({
    'rarity': 'star',
    'member': 'idolized',
    'name': 'id',
    'versions': 'world',
    'is_promo': 'promo',
    'is_original': 'deck',
    'release_date': 'date',
    'favorited': 'heart',
    'collectedcards': 'deck',
})

CARDS_ORDER = [
    'id', 'card_name', 'member', 'cameo_members', 'rarity', 'attribute', 'versions', 'is_promo', 'is_original',
    'release_date',
    'japanese_skill_name', 'skill_type', 'japanese_skill',
    'gacha', 'images', 'arts', 'transparents', 'chibis', 'associated_costume'
]

CARDS_STATISTICS_ORDER = [
    'image', 'image_trained',
] + CARDS_STATS_FIELDS + [
    'skill_type',
]

CARDS_EXCLUDE = [
    'name', 'japanese_name', 'skill_name', 'i_side_skill_type',
    'image_trained', 'art', 'art_trained', 'transparent', 'transparent_trained',
] + CARDS_STATS_FIELDS + [
    'i_skill_note_type', 'skill_stamina', 'skill_duration',
    'skill_percentage', 'skill_alt_percentage', 'i_skill_special',
]

class CardCollection(MagiCollection):
    queryset = models.Card.objects.all()
    title = _('Card')
    plural_title = _('Cards')
    icon = 'deck'
    navbar_link_list = 'girlsbandparty'

    form_class = forms.CardForm
    reportable = False
    blockable = False
    translated_fields = ('name', 'skill_name', )

    _skill_icons = { _i: _c['icon'] for _i, _c in models.Card.SKILL_TYPES.items() }
    _version_images = { _vn: _v['image'] for _vn, _v in models.Account.VERSIONS.items() }
    _origin_to_cuteform = {
        'is_original': 'deck',
        'is_promo': 'promo',
        'is_gacha': 'star',
        'is_event': 'event',
    }
    filter_cuteform = CARD_CUTEFORM
    collectible = [
        models.CollectibleCard,
        models.FavoriteCard,
    ]

    def collectible_to_class(self, model_class):
        cls = super(CardCollection, self).collectible_to_class(model_class)
        if model_class.collection_name == 'favoritecard':
            return to_FavoriteCardCollection(cls)
        return to_CollectibleCardCollection(cls)

    def share_image(self, context, item):
        return 'screenshots/cards.png'

    def to_fields(self, view, item, *args, **kwargs):
        fields = super(CardCollection, self).to_fields(view, item, *args, icons=CARDS_ICONS, images={
            'attribute': u'{static_url}img/i_attribute/{value}.png'.format(
                static_url=RAW_CONTEXT['static_url'],
                value=item.i_attribute,
            ),
        }, **kwargs)
        setSubField(fields, 'rarity', key='type', value='html')
        setSubField(fields, 'rarity', key='value', value=lambda f: rarity_to_stars_images(item.i_rarity))
        return fields

    def buttons_per_item(self, view, *args, **kwargs):
        buttons = super(CardCollection, self).buttons_per_item(view, *args, **kwargs)
        if 'favoritecard' in buttons:
            if view.view == 'list_view':
                buttons['favoritecard']['icon'] = 'star'
        return buttons

    class ItemView(MagiCollection.ItemView):
        queryset = models.Card.objects.all().select_related('associated_costume')
        top_illustration = 'items/cardItem'
        ajax_callback = 'loadCard'

        def to_fields(self, item, extra_fields=None, exclude_fields=None, order=None, *args, **kwargs):
            if extra_fields is None: extra_fields = []
            if exclude_fields is None: exclude_fields = []
            # Add id field
            extra_fields.append(('id', {
                'verbose_name': _(u'ID'),
                'type': 'text',
                'value': item.id,
                'icon': 'id',
            }))
            # Add title field
            title = item.japanese_name if item.japanese_name else (item.name if item.name and get_language() != 'ja' else None)
            value = item.t_name if item.t_name and get_language() != 'ja' and unicode(title) != unicode(item.t_name) else None
            if title or value:
                extra_fields.append(('card_name', {
                    'verbose_name': _('Title'),
                    'type': 'title_text' if title and value else 'text',
                    'title': title,
                    'value': value or title,
                    'icon': 'id',
                }))

            # Add skill details
            if item.i_skill_type:
                extra_fields.append(('japanese_skill', {
                    'verbose_name': _('Skill'),
                    'verbose_name_subtitle': t['Japanese'] if get_language() != 'ja' else None,
                    'icon': item.skill_icon,
                    'type': 'title_text',
                    'title': mark_safe(u'{} <span class="text-muted">({})</span>'.format(item.japanese_skill_type, item.japanese_side_skill_type)
                                       if item.i_side_skill_type else item.japanese_skill_type),
                    'value': item.japanese_full_skill,
                }))
            # Add gacha and events
            for cached_event in (item.cached_events or []):
                extra_fields.append((u'event-{}'.format(cached_event), {
                    'verbose_name': u'{}: {}'.format(
                        _('Event'),
                        cached_event.japanese_name if get_language() == 'ja' else cached_event.name),
                    'icon': 'event',
                    'value': cached_event.image_url,
                    'type': 'image_link',
                    'link': cached_event.item_url,
                    'ajax_link': cached_event.ajax_item_url,
                    'link_text': cached_event.japanese_name if get_language() == 'ja' else cached_event.name,
                }))
            for cached_gacha in (item.cached_gachas or []):
                extra_fields.append((u'gacha-{}'.format(cached_gacha.id), {
                    'image': staticImageURL('gacha.png'),
                    'verbose_name': u'{}: {}'.format(
                        _('Gacha'),
                        cached_gacha.unicode),
                    'value': cached_gacha.image_url,
                    'type': 'image_link',
                    'link': cached_gacha.item_url,
                    'ajax_link': cached_gacha.ajax_item_url,
                    'link_text': cached_gacha.japanese_name if get_language() == 'ja' else cached_gacha.name,
                }))
            # Add images fields
            for image, verbose_name in [('image', _('Icon')), ('art', _('Art')), ('transparent', _('Transparent'))]:
                if getattr(item, image):
                    extra_fields.append((u'{}s'.format(image), {
                        'verbose_name': verbose_name,
                        'type': 'images_links',
                        'images': [{
                            'value': thumbnail_url,
                            'link': image_url,
                            'verbose_name': verbose_name,
                            'link_text': verbose_name,
                        } for image_url, thumbnail_url in [
                            (getattr(item, u'{}_original_url'.format(image)),
                             getattr(item, u'{}_thumbnail_url'.format(image))),
                            (getattr(item, u'{}_trained_original_url'.format(image)),
                             getattr(item, u'{}_trained_thumbnail_url'.format(image))),
                        ] if image_url],
                        'icon': 'pictures',
                    }))
            # Add chibis
            if item.cached_chibis:
                extra_fields.append(('chibis', {
                    'icon': 'pictures',
                    'type': 'images',
                    'verbose_name': _('Chibi'),
                    'images': [{
                        'value': chibi.image_url,
                        'verbose_name': _('Chibi'),
                    } for chibi in item.cached_chibis],
                }))
            # Add cameos
            if item.cached_cameos:
                extra_fields.append(('cameo_members', {
                    'icon': 'users',
                    'verbose_name': _('Cameos'),
                    'type': 'images_links',
                    'images': [{
                        'value': cameo.image_url,
                        'link': cameo.item_url,
                        'ajax_link': cameo.ajax_item_url,
                        'link_text': cameo.name,
                    } for cameo in item.cached_cameos]
                }))
            # Add live2d viewer
            if hasattr(item, 'associated_costume'):
                to_cos_link = lambda text, classes=None: u'<a href="{url}" target="_blank" class="{classes}" data-ajax-url="{ajax_url}" data-ajax-title="{ajax_title}">{text}</a>'.format(
                    url=item.associated_costume.item_url,
                    ajax_url=item.associated_costume.ajax_item_url + "?from_card",
                    ajax_title=string_concat(_("Costume"), " - ", unicode(item)),
                    text=text,
                    classes=classes or '',
                )
                extra_fields.append(('associated_costume', {
                    'icon': 'pictures',
                    'verbose_name': _('Costume'),
                    'type': 'html',
                    'value': mark_safe(u'{} {}'.format(
                        to_cos_link(_('View model'), classes='btn btn-lg btn-secondary'),
                        to_cos_link(u'<img src="{url}" alt="{item} preview">'.format(
                            url=item.associated_costume.preview_image_url,
                            item=unicode(item),
                        )) if item.associated_costume.preview_image_url else '',
                    ))
                }))

            # Exclude fields
            if exclude_fields == 1:
                exclude_fields = []
            else:
                exclude_fields += CARDS_EXCLUDE + (['versions', 'i_skill_type'] if get_language() == 'ja' else [])
            exclude_fields += ['show_art_on_homepage', 'show_trained_art_on_homepage']
            # Order
            if order is None:
                order = CARDS_ORDER

            fields = super(CardCollection.ItemView, self).to_fields(item, *args, extra_fields=extra_fields, exclude_fields=exclude_fields, order=order, **kwargs)
            # Modify existing fields
            # skill name
            setSubField(fields, 'japanese_skill_name', key='verbose_name', value=_('Skill name'))
            setSubField(fields, 'japanese_skill_name', key='icon', value='skill')
            if item.skill_name and get_language() != 'ja' and unicode(item.japanese_skill_name) != unicode(item.t_skill_name):
                setSubField(fields, 'japanese_skill_name', key='type', value='title_text')
                setSubField(fields, 'japanese_skill_name', key='title', value=item.japanese_skill_name)
                setSubField(fields, 'japanese_skill_name', key='value', value=item.t_skill_name)
            # skill deTails
            setSubField(fields, 'skill_type', key='type', value='title_text')
            setSubField(fields, 'skill_type', key='title',
                        value=lambda k: mark_safe(u'{} <span class="text-muted">({})</span>'.format(item.t_skill_type, item.t_side_skill_type)
                        if item.i_side_skill_type else item.t_skill_type))
            setSubField(fields, 'skill_type', key='value', value=item.full_skill)
            setSubField(fields, 'skill_type', key='icon', value=lambda k: item.skill_icon)
            # Totals
            setSubField(fields, 'favorited', key='link', value=u'/users/?favorited_card={}'.format(item.id))
            setSubField(fields, 'favorited', key='ajax_link', value=u'/ajax/users/?favorited_card={}&ajax_modal_only'.format(item.id))
            setSubField(fields, 'collectedcards', key='link', value=u'/accounts/?collected_card={}'.format(item.id))
            setSubField(fields, 'collectedcards', key='ajax_link', value=u'/ajax/accounts/?collected_card={}&ajax_modal_only'.format(item.id))
            # hide is promo, is original
            if not item.is_promo and 'is_promo' in fields:
                del(fields['is_promo'])
            if not item.is_original and 'is_original' in fields:
                del(fields['is_original'])
            return fields

        def buttons_per_item(self, request, context, item):
            buttons = super(CardCollection.ItemView, self).buttons_per_item(request, context, item)
            if request.user.is_authenticated() and request.user.hasPermission('manage_main_items'):
                for field in ['art', 'art_trained']:
                    if getattr(item, field):
                        buttons[u'preview_{}'.format(field)] = {
                            'classes': self.item_buttons_classes + ['staff-only'],
                            'show': True,
                            'url': u'/?preview={}'.format(getattr(item, u'{}_url'.format(field))),
                            'icon': 'link',
                            'title': u'Preview {} on homepage'.format(field.replace('_', ' ')),
                            'has_permissions': True,
                            'open_in_new_window': True,
                        }
            return buttons

    class ListView(MagiCollection.ListView):
        item_template = custom_item_template
        per_line = 2
        page_size = 36
        filter_form = forms.CardFilterForm
        default_ordering = '-release_date,-id'
        ajax_pagination_callback = 'loadCardInList'

        alt_views = MagiCollection.ListView.alt_views + [
            ('icons', { 'verbose_name': string_concat(_('Icons'), ' (', _('Quick add'), ')') }),
            ('statistics', {
                'verbose_name': _('Statistics'),
                'template': 'default_item_table_view',
                'display_style': 'table',
                'display_style_table_fields': [
                    'image', 'image_trained',
                    'performance_min', 'performance_max', 'performance_trained_max',
                    'technique_min', 'technique_max', 'technique_trained_max',
                    'visual_min', 'visual_max', 'visual_trained_max',
                    'overall_min', 'overall_max', 'overall_trained_max',
                    'skill_type',
                ],
            }),
            ('chibis', { 'verbose_name': _('Chibi') }),
            ('art', { 'verbose_name': _('Art') }),
            ('art_trained', { 'verbose_name': string_concat(_('Art'), ' (', _('Trained'), ')') }),
            ('transparent', { 'verbose_name': _('Transparent') }),
        ]

        def get_queryset(self, queryset, parameters, request):
            queryset = super(CardCollection.ListView, self).get_queryset(queryset, parameters, request)
            if request.GET.get('ordering', None) in ['_overall_max', '_overall_trained_max']:
                queryset = queryset.extra(select={
                    '_overall_max': 'performance_max + technique_max + visual_max',
                    '_overall_trained_max': 'performance_trained_max + technique_trained_max + visual_trained_max',
                })
            return queryset

        def extra_context(self, context):
            context['view'] = context['request'].GET.get('view', None)
            if context['view'] == 'icons':
                context['per_line'] = 6
                context['col_size'] = int(math.ceil(12 / context['per_line']))
                context['col_break'] = 'xs'
                for item in context['items']:
                    item.show_item_buttons_as_icons = True
            if context['view'] == 'statistics':
                context['full_width'] = True
                context['include_below_item'] = False
            return context

        def ordering_fields(self, item, only_fields=None, exclude_fields=None, *args, **kwargs):
            if exclude_fields is None: exclude_fields = []
            exclude_fields += ['i_rarity']
            fields = super(CardCollection.ListView, self).ordering_fields(item, *args, only_fields=only_fields, exclude_fields=exclude_fields, **kwargs)
            if '_overall_max' in only_fields:
                fields['overall_max'] = {
                    'verbose_name': string_concat(_('Overall'), ' (', _('Maximum'), ')'),
                    'value': item._overall_max,
                    'type': 'text',
                    'icon': 'skill',
                }
            if '_overall_trained_max' in only_fields:
                fields['overall_trained_max'] = {
                    'verbose_name': string_concat(_('Overall'), ' (', _('Trained'), ', ', _('Maximum'), ')'),
                    'value': item._overall_trained_max,
                    'type': 'text',
                    'icon': 'skill',
                }
            return fields

        def table_fields(self, item, order=None, extra_fields=None, exclude_fields=None, *args, **kwargs):
            if extra_fields is None: extra_fields = []
            if exclude_fields is None: exclude_fields = []
            if order is None:
                order = CARDS_STATISTICS_ORDER
            extra_fields += [
                (u'overall_{}'.format(suffix), { 'value': getattr(item, u'overall_{}'.format(suffix)) })
                for suffix in ['min', 'max', 'trained_max']
            ]
            fields = super(CardCollection.ListView, self).table_fields(
                item, *args, exclude_fields=1, extra_fields=extra_fields, order=order, **kwargs)
            for field_name in ['image', 'image_trained']:
                if item.trainable or 'trained' not in field_name:
                    setSubField(fields, field_name, key='type', value='image_link')
                    setSubField(fields, field_name, key='link', value=item.item_url)
                    setSubField(fields, field_name, key='ajax_link', value=item.ajax_item_url)
                    setSubField(fields, field_name, key='link_text', value=unicode(item))
            # Hide trained fields for cards that are not trainable
            if not item.trainable:
                for field_name in ['image_trained', 'performance_trained_max', 'technique_trained_max', 'visual_trained_max', 'overall_trained_max']:
                    setSubField(fields, field_name, key='type', value='text')
                    setSubField(fields, field_name, key='value', value='')
            return fields

        def table_fields_headers_sections(self, view):
            return [
                ('', '', 2),
                ('performance', _('Performance'), 3),
                ('technique', _('Technique'), 3),
                ('visual', _('Visual'), 3),
                ('overall', _('Overall'), 3),
                ('skill', _('Skill'), 1),
            ]

        def table_fields_headers(self, fields, view=None):
            return [('image', ''), ('image_trained', '')] + [
                (u'{}_{}'.format(name, suffix), verbose_name)
                for name in ['performance', 'technique', 'visual', 'overall']
                for suffix, verbose_name in [
                        ('min', _('Min')), ('max', _('Max')),
                        ('trained_max', _('Trained')),
                ]] + [('skill_type', '')]

    def _extra_context_for_form(self, context):
        if 'js_variables' not in context:
            context['js_variables'] = {}
        context['js_variables']['all_variables'] = jsv(models.Card.ALL_VARIABLES)
        context['js_variables']['variables_per_skill_type'] = jsv(models.Card.VARIABLES_PER_SKILL_TYPES)
        context['js_variables']['special_cases_variables'] = jsv(models.Card.SPECIAL_CASES_VARIABLES)
        context['js_variables']['template_per_skill_type'] = jsv(models.Card.TEMPLATE_PER_SKILL_TYPES)
        context['js_variables']['special_cases_template'] = jsv(models.Card.SPECIAL_CASES_TEMPLATE)

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']
        multipart = True
        ajax_callback = 'loadCardForm'

        def extra_context(self, context):
            super(CardCollection.AddView, self).extra_context(context)
            self.collection._extra_context_for_form(context)

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']
        multipart = True
        ajax_callback = 'loadCardForm'

        def extra_context(self, context):
            super(CardCollection.EditView, self).extra_context(context)
            self.collection._extra_context_for_form(context)

        def to_translate_form_class(self):
            super(CardCollection.EditView, self).to_translate_form_class()
            self._translate_form_class = forms.to_translate_card_form_class(self._translate_form_class)

############################################################
# Event Participation Collection

EVENT_PARTICIPATIONS_ICONS = {
    'score': 'scoreup',
    'ranking': 'trophy',
    'song_score': 'song',
    'song_ranking': 'trophy',
    'is_trial_master_completed': 'achievement',
    'is_trial_master_ex_completed': 'achievement',
    'screenshot': 'pictures',
}

def to_EventParticipationCollection(cls):
    class _EventParticipationCollection(cls):
        title = _('Participated event')
        plural_title = _('Participated events')
        collectible_tab_name = _('Events')
        multipart = True
        show_edit_button_superuser_only = True
        form_class = forms.to_EventParticipationForm(cls)
        reportable = True
        report_allow_delete = False

        report_edit_templates = OrderedDict([
            ('Unrealistic Score', 'Your score is unrealistic, so we edited it. If this was a mistake, please upload a screenshot of your game to the details of your event participation to prove your score and change it back. Thank you for your understanding.'),
            ('Unrealistic Ranking', 'Your ranking is unrealistic, so we edited it. If this was a mistake, please upload a screenshot of your game to the details of your event participation to prove your score and change it back. Thank you for your understanding.'),
            ('Unrealistic Song Score', 'Your song score is unrealistic, so we edited it. If this was a mistake, please upload a screenshot of your game to the details of your event participation to prove your score and change it back. Thank you for your understanding.'),
            ('Unrealistic Song Ranking', 'Your song ranking is unrealistic, so we edited it. If this was a mistake, please upload a screenshot of your game to the details of your event participation to prove your score and change it back. Thank you for your understanding.'),
        ])

        filter_cuteform = {
            'i_version': {
                'to_cuteform': lambda k, v: AccountCollection._version_images[k],
                'image_folder': 'language',
                'transform': CuteFormTransform.ImagePath,
            },
            'is_trial_master_completed': { 'type': CuteFormType.YesNo, },
            'is_trial_master_ex_completed': { 'type': CuteFormType.YesNo, },
        }

        def to_fields(self, view, item, *args, **kwargs):
            return super(_EventParticipationCollection, self).to_fields(view, item, *args, icons=EVENT_PARTICIPATIONS_ICONS, **kwargs)

        class AddView(cls.AddView):
            unique_per_owner = True
            add_to_collection_variables = cls.AddView.add_to_collection_variables + [
                'i_type',
            ]

        class ListView(cls.ListView):
            per_line = 3
            default_ordering = '-event__start_date'
            filter_form = forms.to_EventParticipationFilterForm(cls)
            show_item_buttons_as_icons = True
            show_item_buttons_justified = False

            alt_views = cls.ListView.alt_views + [
                ('leaderboard', {
                    'verbose_name': _('Leaderboard'),
                    'template': 'eventParticipationLeaderboard',
                    'per_line': 1,
                    'full_width': True,
                }),
            ]

            def get_queryset(self, queryset, parameters, request):
                queryset = super(_EventParticipationCollection.ListView, self).get_queryset(queryset, parameters, request)
                if request.GET.get('view', None) == 'leaderboard':
                    queryset = queryset.select_related('account')
                    if request.GET.get('i_version', None) is not None:
                        queryset = queryset.exclude(ranking__isnull=True).exclude(ranking=0)
                return queryset

            def extra_context(self, context):
                if context['view'] == 'leaderboard':
                    context['show_relevant_fields_on_ordering'] = False

    return _EventParticipationCollection

############################################################
# Event Collection

EVENT_ITEM_FIELDS_ORDER = [
    'name', 'japanese_name', 'type', 'participations',
] + [
    u'{}{}'.format(_v['prefix'], _f) for _v in models.Account.VERSIONS.values()
    for _f in models.Event.FIELDS_PER_VERSION
] + [
    'boost_attribute', 'boost_members', 'cards',
]

EVENT_ICONS = {
    'name': 'event',
    'participations': 'contest',
    'start_date': 'date', 'end_date': 'date',
    'english_start_date': 'date', 'english_end_date': 'date',
    'taiwanese_start_date': 'date', 'taiwanese_end_date': 'date',
    'korean_start_date': 'date', 'korean_end_date': 'date',
    'type': 'toggler',
}

EVENT_CUTEFORM = {
        'main_card': {
            'to_cuteform': lambda k, v: v.image_url,
            'title': _('Card'),
            'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
        },
        'secondary_card': {
            'to_cuteform': lambda k, v: v.image_url,
            'title': _('Card'),
            'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
        },
        'i_boost_attribute': {
            'image_folder': 'i_attribute',
        },
        'version': {
            'to_cuteform': lambda k, v: CardCollection._version_images[k],
            'image_folder': 'language',
            'transform': CuteFormTransform.ImagePath,
        },
    }

EVENT_LIST_ITEM_CUTEFORM = EVENT_CUTEFORM.copy()
EVENT_LIST_ITEM_CUTEFORM['boost_members'] = {
    'to_cuteform': lambda k, v: FAVORITE_CHARACTERS_IMAGES[k],
    'title': _('Boost members'),
    'extra_settings': {
        'modal': 'true',
        'modal-text': 'true',
    },
}

class EventCollection(MagiCollection):
    queryset = models.Event.objects.all()
    title = _('Event')
    plural_title = _('Events')
    icon = 'event'
    form_class = forms.EventForm
    multipart = True
    reportable = False
    blockable = False
    translated_fields = ('name', 'stamp_translation', )
    navbar_link_list = 'girlsbandparty'

    filter_cuteform = EVENT_LIST_ITEM_CUTEFORM

    collectible = models.EventParticipation

    def collectible_to_class(self, model_class):
        cls = super(EventCollection, self).collectible_to_class(model_class)
        if model_class.collection_name == 'eventparticipation':
            return to_EventParticipationCollection(cls)
        return cls

    def to_fields(self, view, item, *args, **kwargs):
        fields = super(EventCollection, self).to_fields(view, item, *args, icons=EVENT_ICONS, images={
            'boost_attribute': u'{static_url}img/i_attribute/{value}.png'.format(
                static_url=RAW_CONTEXT['static_url'],
                value=item.i_boost_attribute,
            ),
            'english_image': staticImageURL('language/world.png'),
            'taiwanese_image': staticImageURL('language/zh-hant.png'),
            'korean_image': staticImageURL('language/kr.png'),
            'rare_stamp': staticImageURL('stamp.png'),
            'stamp_translation': staticImageURL('stamp.png'),
            'english_rare_stamp': staticImageURL('stamp.png'),
            'taiwanese_rare_stamp': staticImageURL('stamp.png'),
            'korean_rare_stamp': staticImageURL('stamp.png'),
        }, **kwargs)
        if get_language() == 'ja' and 'name' in fields and 'japanese_name' in fields:
            setSubField(fields, 'japanese_name', key='verbose_name', value=fields['name']['verbose_name'])
            del(fields['name'])
        if item.name == item.japanese_name and 'japanese_name' in fields:
            del(fields['japanese_name'])
        setSubField(fields, 'start_date', key='timezones', value=['Asia/Tokyo', 'Local time'])
        setSubField(fields, 'end_date', key='timezones', value=['Asia/Tokyo', 'Local time'])

        setSubField(fields, 'english_start_date', key='timezones', value=['UTC', 'Local time'])
        setSubField(fields, 'english_end_date', key='timezones', value=['UTC', 'Local time'])

        setSubField(fields, 'taiwanese_start_date', key='timezones', value=['Asia/Taipei', 'Local time'])
        setSubField(fields, 'taiwanese_end_date', key='timezones', value=['Asia/Taipei', 'Local time'])

        setSubField(fields, 'korean_start_date', key='timezones', value=['Asia/Seoul', 'Local time'])
        setSubField(fields, 'korean_end_date', key='timezones', value=['Asia/Seoul', 'Local time'])

        if get_language() in models.ALT_LANGUAGES_EXCEPT_JP_KEYS and unicode(item.name) != unicode(item.t_name):
            setSubField(fields, 'name', key='value', value=mark_safe(u'{}<br><span class="text-muted">{}</span>'.format(item.name, item.t_name)))

        return fields

    class ListView(MagiCollection.ListView):
        per_line = 2
        default_ordering = '-start_date'

        filter_form = forms.EventFilterForm
        show_collect_button = {
            'eventparticipation': False,
        }
        alt_views = MagiCollection.ListView.alt_views + [
            ('stamps', {
                'verbose_name': _('Rare stamp'),
                'template': 'eventStampItem',
                'per_line': 4,
            }),
        ]

    class ItemView(MagiCollection.ItemView):
        template = 'default'
        ajax_callback = 'loadEventGacha'

        def get_queryset(self, queryset, parameters, request):
            queryset = super(EventCollection.ItemView, self).get_queryset(queryset, parameters, request)
            queryset = queryset.select_related('main_card', 'secondary_card').prefetch_related(Prefetch('boost_members', to_attr='all_members'), Prefetch('gachas', to_attr='all_gachas'), Prefetch('gift_songs', to_attr='all_gifted_songs'))
            return queryset

        def extra_context(self, context):
            if 'js_variables' not in context:
                context['js_variables'] = {}
            context['js_variables']['versions_prefixes'] = jsv(models.Account.VERSIONS_PREFIXES)
            context['js_variables']['fields_per_version'] = jsv(models.Event.FIELDS_PER_VERSION)

        def to_fields(self, item, order=None, extra_fields=None, exclude_fields=None, *args, **kwargs):
            if extra_fields is None: extra_fields = []
            if exclude_fields is None: exclude_fields = []
            if order is None: order = []
            order = EVENT_ITEM_FIELDS_ORDER + order
            for version in models.Account.VERSIONS.values():
                status = getattr(item, u'{}status'.format(version['prefix']))
                if status and status != 'ended':
                    start_date = getattr(item, u'{}start_date'.format(version['prefix']))
                    end_date = getattr(item, u'{}end_date'.format(version['prefix']))
                    extra_fields += [
                        (u'{}countdown'.format(version['prefix']), {
                            'verbose_name': _('Countdown'),
                            'value': mark_safe(u'<span class="fontx1-5 countdown" data-date="{date}" data-format="{sentence}"></h4>').format(
                                date=torfc2822(end_date if status == 'current' else start_date),
                                sentence=_('{time} left') if status == 'current' else _('Starts in {time}'),
                            ),
                            'icon': 'times',
                            'type': 'html',
                        }),
                    ]
            extra_fields.append(('image', {
                'image': staticImageURL('language/ja.png'),
                'verbose_name': _('Japanese version'),
                'type': 'image',
                'value': item.image_url,
            }))
            if len(item.all_gachas):
                for gacha in item.all_gachas:
                    extra_fields.append((u'gacha-{}'.format(gacha.id), {
                        'image': staticImageURL('gacha.png'),
                        'verbose_name': u'{}: {}'.format(
                            _('Gacha'),
                            unicode(gacha),
                        ),
                        'value': gacha.image_url,
                        'type': 'image_link',
                        'link': gacha.item_url,
                        'ajax_link': gacha.ajax_item_url,
                        'link_text': unicode(gacha),
                    }))
            if len(item.all_members):
                extra_fields.append(('boost_members', {
                    'icon': 'users',
                    'verbose_name': _('Boost Members'),
                    'type': 'images_links',
                    'images': [{
                        'value': member.square_image_url,
                        'link': member.item_url,
                        'ajax_link': member.ajax_item_url,
                        'link_text': unicode(member),
                    } for member in item.all_members]
                }))
            if item.main_card_id or item.secondary_card_id:
                extra_fields.append(('cards', {
                    'icon': 'cards',
                    'verbose_name': _('Cards'),
                    'type': 'images_links',
                    'images': [{
                        'value': card.image_url,
                        'link': card.item_url,
                        'ajax_link': card.ajax_item_url,
                        'link_text': unicode(card),
                    } for card in [item.main_card, item.secondary_card] if card is not None]
                }))
            if len(item.all_gifted_songs):
                for song in item.all_gifted_songs:
                    extra_fields.append(('song-{}'.format(song.id), {
                        'icon': 'song',
                        'verbose_name': u'{}: {}'.format(
                            _('Gift song'),
                            unicode(song),
                        ),
                        'value': song.image_url,
                        'type': 'image_link',
                        'link': song.item_url,
                        'ajax_link': song.ajax_item_url,
                        'link_text': unicode(song),
                    }))
            for i_version, version in enumerate(models.Account.VERSIONS.values()):
                if not getattr(item, u'{}image'.format(version['prefix'])) and getattr(item, u'{}start_date'.format(version['prefix'])):
                    extra_fields.append(('{}image'.format(version['prefix']), {
                        'image': staticImageURL(version['image'], folder='language', extension='png'),
                        'verbose_name': version['translation'],
                        'type': 'html',
                        'value': u'<hr>',
                    }))
                if item.stamp_translation:
                    extra_fields.append(('{}stamp_translation'.format(version['prefix']), {
                        'image': staticImageURL('stamp.png'),
                        'verbose_name': _('Stamp translation'),
                        'type': 'text',
                        'value': item.t_stamp_translation,
                    }))
                status = getattr(item, u'{}status'.format(version['prefix']))
                if status == 'ended':
                    extra_fields.append(('{}leaderboard'.format(version['prefix']), {
                        'icon': 'contest',
                        'verbose_name': _('Leaderboard'),
                        'type': 'button',
                        'link_text': mark_safe('<i class="flaticon-contest"></i>'),
                        'value': u'/eventparticipations/?event={}&view=leaderboard&ordering=ranking&i_version={}'.format(item.id, i_version),
                        'ajax_link': u'/ajax/eventparticipations/?event={}&view=leaderboard&ordering=ranking&i_version={}&ajax_modal_only'.format(item.id, i_version),
                        'title': u'{} - {}'.format(unicode(item), _('Leaderboard')),
                    }))

            exclude_fields += ['c_versions', 'japanese_name']
            fields = super(EventCollection.ItemView, self).to_fields(
                item, *args, order=order, extra_fields=extra_fields, exclude_fields=exclude_fields, **kwargs)

            setSubField(fields, 'name', key='type', value='text' if get_language() == 'ja' else 'title_text')
            setSubField(fields, 'name', key='title', value=item.t_name)
            setSubField(fields, 'name', key='value', value=item.japanese_name)

            for version in models.Account.VERSIONS.values():
                setSubField(fields, u'{}image'.format(version['prefix']), key='verbose_name', value=version['translation'])
                setSubField(fields, u'{}start_date'.format(version['prefix']), key='verbose_name', value=_('Beginning'))
                setSubField(fields, u'{}end_date'.format(version['prefix']), key='verbose_name', value=_('End'))
                setSubField(fields, u'{}rare_stamp'.format(version['prefix']), key='verbose_name', value=_('Rare stamp'))

            if 'participations' in fields:
                setSubField(fields, 'participations', key='link', value=u'{}&view=leaderboard&ordering=id&reverse_order=on'.format(fields['participations']['link']))
                setSubField(fields, 'participations', key='ajax_link', value=u'{}&view=leaderboard&ordering=id&reverse_order=on&ajax_modal_only'.format(fields['participations']['ajax_link']))

            return fields

    # For AddView and EditView
    def _after_save(self, request, instance, type=None):
        if instance.main_card and instance.main_card.id:
            instance.main_card.force_update_cache('events')
        previous_main_card_id = getattr(instance, 'previous_main_card_id', None)
        if previous_main_card_id:
            previous_main_card = models.Card.objects.get(id=previous_main_card_id)
            previous_main_card.force_update_cache('events')
        if instance.secondary_card and instance.secondary_card.id:
            instance.secondary_card.force_update_cache('events')
        previous_secondary_card_id = getattr(instance, 'previous_secondary_card_id', None)
        if previous_secondary_card_id:
            previous_secondary_card = models.Card.objects.get(id=previous_secondary_card_id)
            previous_secondary_card.force_update_cache('events')
        return instance

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']
        savem2m = True
        filter_cuteform = EVENT_CUTEFORM

        def after_save(self, request, instance, type=None):
            instance = super(EventCollection.AddView, self).after_save(request, instance, type=type)
            return self.collection._after_save(request, instance)

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']
        savem2m = True
        filter_cuteform = EVENT_CUTEFORM

        def to_translate_form_class(self):
            super(EventCollection.EditView, self).to_translate_form_class()
            self._translate_form_class = forms.to_translate_event_form_class(self._translate_form_class)

        def after_save(self, request, instance, type=None):
            instance = super(EventCollection.EditView, self).after_save(request, instance, type=type)
            return self.collection._after_save(request, instance)

############################################################
# Gacha Collection

GACHA_ICONS = {
    'start_date': 'date',
    'end_date': 'date',
    'english_start_date': 'date', 'english_end_date': 'date',
    'taiwanese_start_date': 'date', 'taiwanese_end_date': 'date',
    'korean_start_date': 'date', 'korean_end_date': 'date',
    'event': 'event',
    'limited': 'toggler',
    'versions': 'world',
}

GACHA_ITEM_FIELDS_ORDER = [
    'name',
] + [
    u'{}{}'.format(_v['prefix'], _f) for _v in models.Account.VERSIONS.values()
    for _f in models.Gacha.FIELDS_PER_VERSION
] + [
 'attribute', 'limited', 'cards',
]

class GachaCollection(MagiCollection):
    queryset = models.Gacha.objects.all()
    icon = 'star'
    title = _('Gacha')
    plural_title = _('Gacha')
    form_class = forms.GachaForm
    multipart = True
    navbar_link_list = 'girlsbandparty'
    reportable = False
    blockable = False
    translated_fields = ('name', )

    filter_cuteform = {
        'featured_member': {
            'to_cuteform': lambda k, v: FAVORITE_CHARACTERS_IMAGES[k],
            'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
        },
        'i_attribute': {},
        'event': {
            'to_cuteform': lambda k, v: v.image_url,
            'title': _('Event'),
            'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
        },
        'is_limited': {
            'type': CuteFormType.OnlyNone,
        },
        'version': {
            'to_cuteform': lambda k, v: CardCollection._version_images[k],
            'image_folder': 'language',
            'transform': CuteFormTransform.ImagePath,
        },
    }

    def to_fields(self, view, item, in_list=False, exclude_fields=None, *args, **kwargs):
        if exclude_fields is None: exclude_fields = []
        exclude_fields.append('dreamfes')
        fields = super(GachaCollection, self).to_fields(view, item, *args, icons=GACHA_ICONS, images={
            'name': staticImageURL('gacha.png'),
            'japanese_name': staticImageURL('gacha.png'),
            'attribute': u'{static_url}img/i_attribute/{value}.png'.format(
                static_url=RAW_CONTEXT['static_url'],
                value=item.i_attribute,
            ),
            'english_image': staticImageURL('language/world.png'),
            'taiwanese_image': staticImageURL('language/zh-hant.png'),
            'korean_image': staticImageURL('language/kr.png'),
        }, exclude_fields=exclude_fields, **kwargs)
        if get_language() == 'ja' or unicode(item.t_name) == unicode(item.japanese_name):
            setSubField(fields, 'name', key='value', value=item.japanese_name)
        else:
            setSubField(fields, 'name', key='type', value='title_text')
            setSubField(fields, 'name', key='title', value=item.t_name)
            setSubField(fields, 'name', key='value', value=item.japanese_name)

        setSubField(fields, 'start_date', key='timezones', value=['Asia/Tokyo', 'Local time'])
        setSubField(fields, 'end_date', key='timezones', value=['Asia/Tokyo', 'Local time'])

        setSubField(fields, 'english_start_date', key='timezones', value=['UTC', 'Local time'])
        setSubField(fields, 'english_end_date', key='timezones', value=['UTC', 'Local time'])

        setSubField(fields, 'taiwanese_start_date', key='timezones', value=['Asia/Taipei', 'Local time'])
        setSubField(fields, 'taiwanese_end_date', key='timezones', value=['Asia/Taipei', 'Local time'])

        setSubField(fields, 'korean_start_date', key='timezones', value=['Asia/Seoul', 'Local time'])
        setSubField(fields, 'korean_end_date', key='timezones', value=['Asia/Seoul', 'Local time'])

        setSubField(fields, 'event', key='type', value='image_link')
        setSubField(fields, 'event', key='value', value=lambda f: item.event.image_url)
        setSubField(fields, 'event', key='link_text', value=lambda f: item.event.japanese_name if get_language() == 'ja' else item.event.name)
        return fields

    class ItemView(MagiCollection.ItemView):
        template = 'default'
        ajax_callback = 'loadEventGacha'

        def get_queryset(self, queryset, parameters, request):
            queryset = super(GachaCollection.ItemView, self).get_queryset(queryset, parameters, request)
            queryset = queryset.select_related('event').prefetch_related(Prefetch('cards', to_attr='all_cards'))
            return queryset

        def extra_context(self, context):
            if 'js_variables' not in context:
                context['js_variables'] = {}
            context['js_variables']['versions_prefixes'] = jsv(models.Account.VERSIONS_PREFIXES)
            context['js_variables']['fields_per_version'] = jsv(models.Gacha.FIELDS_PER_VERSION)

        def to_fields(self, item, extra_fields=None, exclude_fields=None, order=None, *args, **kwargs):
            if extra_fields is None: extra_fields = []
            if exclude_fields is None: exclude_fields = []
            if order is None: order = []
            order = GACHA_ITEM_FIELDS_ORDER + order
            for version in models.Account.VERSIONS.values():
                status = getattr(item, u'{}status'.format(version['prefix']))
                if status and status != 'ended':
                    start_date = getattr(item, u'{}start_date'.format(version['prefix']))
                    end_date = getattr(item, u'{}end_date'.format(version['prefix']))
                    extra_fields += [
                        (u'{}countdown'.format(version['prefix']), {
                            'verbose_name': _('Countdown'),
                            'value': mark_safe(u'<span class="fontx1-5 countdown" data-date="{date}" data-format="{sentence}"></h4>').format(
                                date=torfc2822(end_date if status == 'current' else start_date),
                                sentence=_('{time} left') if status == 'current' else _('Starts in {time}'),
                            ),
                            'icon': 'times',
                            'type': 'html',
                        }),
                    ]
            extra_fields.append(('image', {
                'image': staticImageURL('language/ja.png'),
                'verbose_name': _('Japanese version'),
                'type': 'image',
                'value': item.image_url,
            }))
            exclude_fields += ['japanese_name', 'c_versions']
            if len(item.all_cards):
                extra_fields.append(('cards', {
                    'icon': 'cards',
                    'verbose_name': _('Cards'),
                    'type': 'images_links',
                    'images': [{
                        'value': card.image_url,
                        'link': card.item_url,
                        'ajax_link': card.ajax_item_url,
                        'link_text': unicode(card),
                    } for card in item.all_cards],
                }))
            for version in models.Account.VERSIONS.values():
                if not getattr(item, u'{}image'.format(version['prefix'])) and getattr(item, u'{}start_date'.format(version['prefix'])):
                    extra_fields.append(('{}image'.format(version['prefix']), {
                        'image': staticImageURL(version['image'], folder='language', extension='png'),
                        'verbose_name': version['translation'],
                        'type': 'html',
                        'value': u'<hr>',
                    }))
            fields = super(GachaCollection.ItemView, self).to_fields(item, *args, extra_fields=extra_fields, exclude_fields=exclude_fields, order=order, **kwargs)
            setSubField(fields, 'limited', key='verbose_name', value=_('Gacha type'))
            setSubField(fields, 'limited', key='type', value='text')
            setSubField(fields, 'limited', key='value', value=(
                _('Limited') if item.limited
                else (models.DREAMFES_PER_LANGUAGE.get(get_language(), 'Dream festival')
                      if item.dreamfes else _('Permanent'))))
            for version in models.Account.VERSIONS.values():
                setSubField(fields, u'{}image'.format(version['prefix']), key='verbose_name', value=version['translation'])
                setSubField(fields, u'{}start_date'.format(version['prefix']), key='verbose_name', value=_('Beginning'))
                setSubField(fields, u'{}end_date'.format(version['prefix']), key='verbose_name', value=_('End'))
            return fields

    class ListView(MagiCollection.ListView):
        default_ordering = '-start_date'
        per_line = 2
        filter_form = forms.GachaFilterForm

    def _after_save(self, request, instance):
        for card in instance.cards.all():
            card.force_update_cache('gachas')
        return instance

    class AddView(MagiCollection.AddView):
        savem2m = True
        staff_required = True
        permissions_required = ['manage_main_items']

        def after_save(self, request, instance, type=None):
            return self.collection._after_save(request, instance)

    class EditView(MagiCollection.EditView):
        savem2m = True
        staff_required = True
        permissions_required = ['manage_main_items']

        def after_save(self, request, instance):
            return self.collection._after_save(request, instance)

        def to_translate_form_class(self):
            super(GachaCollection.EditView, self).to_translate_form_class()
            self._translate_form_class = forms.to_translate_gacha_form_class(self._translate_form_class)

############################################################
# Played songs Collection

PLAYED_SONGS_ICONS = {
    'score': 'scoreup',
    'full_combo': 'combo',
    'all_perfect': 'combo',
    'screenshot': 'pictures',
}

def to_PlayedSongCollection(cls):
    _filter_cuteform = dict(_song_cuteform.items() + [
        ('full_combo', {
            'type': CuteFormType.YesNo,
        }),
        ('all_perfect', {
            'type': CuteFormType.YesNo,
        }),
        ('i_difficulty', {
            'to_cuteform': lambda k, v: models.PlayedSong.DIFFICULTY_CHOICES[k][0],
            'image_folder': 'songs',
            'transform': CuteFormTransform.ImagePath,
        }),
        ('i_version', {
            'to_cuteform': lambda k, v: AccountCollection._version_images[k],
            'image_folder': 'language',
            'transform': CuteFormTransform.ImagePath,
        }),
    ])

    class _PlayedSongCollection(cls):
        title = _('Played song')
        plural_title = _('Played songs')
        collectible_tab_name = _('Songs')
        multipart = True
        form_class = forms.to_PlayedSongForm(cls)
        show_edit_button_superuser_only = True
        reportable = True
        report_allow_delete = False

        report_edit_templates = OrderedDict([
            ('Unrealistic Score', 'Your score is unrealistic, so we edited it. If this was a mistake, please upload a screenshot of your game to the details of your played song to prove your score and change it back. Thank you for your understanding.'),
        ])

        filter_cuteform = _filter_cuteform

        def to_fields(self, view, item, *args, **kwargs):
            fields = super(_PlayedSongCollection, self).to_fields(view, item, *args, icons=PLAYED_SONGS_ICONS, images={
                'difficulty': item.difficulty_image_url,
            }, **kwargs)
            setSubField(fields, 'difficulty', key='value', value=item.t_difficulty)
            return fields

        class ListView(cls.ListView):
            default_ordering = 'song__expert_difficulty,song_id,-i_difficulty'
            filter_form = forms.to_PlayedSongFilterForm(cls)
            item_template = 'default_item_table_view'
            display_style = 'table'
            display_style_table_fields = ['image', 'difficulty', 'score', 'full_combo', 'all_perfect', 'screenshot']
            show_item_buttons = True
            show_item_buttons_as_icons = True
            show_item_buttons_justified = False

            filter_cuteform = _filter_cuteform.copy()
            filter_cuteform['screenshot'] = {
                'type': CuteFormType.YesNo,
            }

            alt_views = cls.ListView.alt_views + [
                ('leaderboard', {
                    'verbose_name': _('Leaderboard'),
                    'display_style': 'row',
                    'template': 'playedSongLeaderboard',
                }),
            ]

            def get_queryset(self, queryset, parameters, request):
                queryset = super(_PlayedSongCollection.ListView, self).get_queryset(queryset, parameters, request)
                if request.GET.get('view', None) == 'leaderboard':
                    queryset = queryset.select_related('account')
                return queryset

            def table_fields(self, item, *args, **kwargs):
                fields = super(_PlayedSongCollection.ListView, self).table_fields(item, *args, **kwargs)
                setSubField(fields, 'image', key='verbose_name', value=_('Song'))
                setSubField(fields, 'image', key='type', value='image_link')
                setSubField(fields, 'image', key='link', value=item.song.item_url)
                setSubField(fields, 'image', key='link_text', value=unicode(item.song))
                setSubField(fields, 'image', key='ajax_link', value=item.song.ajax_item_url)
                setSubField(fields, 'difficulty', key='type', value='image')
                setSubField(fields, 'difficulty', key='value', value=lambda k: item.difficulty_image_url)
                setSubField(fields, 'screenshot', key='type', value='html')
                setSubField(fields, 'screenshot', key='value', value=u'<a href="{url}" target="_blank"><div class="screenshot_preview" style="background-image: url(\'{url}\')"></div></a>'.format(url=item.screenshot_url) if item.screenshot else '')
                return fields

            def table_fields_headers(self, fields, view=None):
                if view is None:
                    headers = MagiCollection.ListView.table_fields_headers(self, fields, view=view)
                    headers[0] = ('image', _('Image'))
                    return headers
                return []

            def extra_context(self, context):
                if context['view'] == 'quick_edit':
                    context['include_below_item'] = False
                if context['view'] == 'leaderboard':
                    context['include_below_item'] = False
                    context['show_relevant_fields_on_ordering'] = False

    return _PlayedSongCollection

############################################################
# Songs Collection

_song_cuteform = {
    'i_band': {
        'image_folder': 'band',
        'to_cuteform': 'value',
        'title': _('Band'),
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
    'event': {
        'to_cuteform': lambda k, v: v.image_url,
        'title': _('Event'),
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
    'version': {
        'to_cuteform': lambda k, v: CardCollection._version_images[k],
        'image_folder': 'language',
        'transform': CuteFormTransform.ImagePath,
    },
}

SONG_ICONS = {
    'japanese_name': 'song',
    'name': 'world',
    'romaji_name': 'song',
    'itunes_id': 'play',
    'length': 'times',
    'unlock': 'perfectlock',
    'bpm': 'hp',
    'release_date': 'date',
    'event': 'event',
    'versions': 'world',
    'played': 'contest',
}

class SongCollection(MagiCollection):
    queryset = models.Song.objects.all()
    title = _('Song')
    plural_title = _('Songs')
    multipart = True
    icon = 'song'
    reportable = False
    blockable = False
    translated_fields = ('name', )
    navbar_link_list = 'bangdream'

    types = {
        _unlock: {
            'title': u'Unlock - {}'.format(_info['translation']),
            'form_class': forms.unlock_to_form(_unlock),
        }
        for _unlock, _info in models.Song.UNLOCK.items()
    }

    filter_cuteform = _song_cuteform

    collectible = models.PlayedSong

    def collectible_to_class(self, model_class):
        cls = super(SongCollection, self).collectible_to_class(model_class)
        if model_class.collection_name == 'playedsong':
            return to_PlayedSongCollection(cls)
        return cls

    def to_fields(self, view, item, *args, **kwargs):
        fields = super(SongCollection, self).to_fields(
            view, item, *args, icons=SONG_ICONS, **kwargs)
        for fieldName in (
                ((['japanese_name', 'romaji_name', 'name']
                 if get_language() == 'ja' else ['romaji_name']) if view.view == 'item_view' else [])
                + ['band', 'unlock_variables', 'is_cover']
                + [f for f, t in models.Song.SONGWRITERS_DETAILS]
                + ((list(chain.from_iterable(
                    (u'{}_notes'.format(d), u'{}_difficulty'.format(d))
                    for d, t in models.Song.DIFFICULTIES))) if view.view == 'item_view' else [])
        ):
            if fieldName in fields:
                del(fields[fieldName])

        setSubField(fields, 'japanese_name', key='verbose_name', value=_('Song'))
        setSubField(fields, 'japanese_name', key='type', value='title_text')
        setSubField(fields, 'japanese_name', key='title', value=item.japanese_name)
        setSubField(fields, 'japanese_name', key='value', value=
                    u'({})'.format(_('Cover') if item.is_cover else _('Original')))

        setSubField(fields, 'length', key='value', value=lambda f: item.length_in_minutes)
        setSubField(fields, 'unlock', key='value', value=item.unlock_sentence)

        setSubField(fields, 'event', key='type', value='image_link')
        setSubField(fields, 'event', key='value', value=lambda f: item.event.image_url)
        setSubField(fields, 'event', key='link_text', value=lambda f: item.event.japanese_name if get_language() == 'ja' else item.event.name)
        return fields

    class ListView(MagiCollection.ListView):
        per_line = 3
        filter_form = forms.SongFilterForm
        default_ordering = '-release_date'
        show_collect_button = {
            'playedsong': False,
        }

        filter_cuteform = dict(_song_cuteform.items() + [
            ('is_cover', {
                'type': CuteFormType.OnlyNone,
            }),
        ])

        def to_fields(self, item, *args, **kwargs):
            fields = super(SongCollection.ListView, self).to_fields(item, *args, **kwargs)
            for difficulty, verbose_name in models.Song.DIFFICULTIES:
                image = lambda f: u'{static_url}img/songs/{difficulty}.png'.format(
                    static_url=RAW_CONTEXT['static_url'],
                    difficulty=difficulty,
                )
                setSubField(fields, u'{}_notes'.format(difficulty), key='image',
                            value=image)
                setSubField(fields, u'{}_difficulty'.format(difficulty), key='image',
                            value=image)
            return fields

    class ItemView(MagiCollection.ItemView):
        template = 'default'
        top_illustration = 'include/songTopIllustration'
        ajax_callback = 'loadSongItem'

        def get_queryset(self, queryset, parameters, request):
            queryset = super(SongCollection.ItemView, self).get_queryset(queryset, parameters, request)
            queryset = queryset.select_related('event')
            return queryset

        def to_fields(self, item, *args, **kwargs):
            fields = super(SongCollection.ItemView, self).to_fields(item, *args, **kwargs)
            note_image = u'{}img/note.png'.format(RAW_CONTEXT['static_url'])
            for difficulty, verbose_name in models.Song.DIFFICULTIES:
                notes = getattr(item, u'{}_notes'.format(difficulty), None)
                difficulty_level = getattr(item, u'{}_difficulty'.format(difficulty), None)
                if notes or difficulty_level:
                    fields[difficulty] = {
                        'verbose_name': verbose_name,
                        'type': 'html',
                        'value': mark_safe(u'{big_images}{small_images}<br />{notes}'.format(
                            difficulty_level=difficulty_level,
                            big_images=(u'<img src="{}" class="song-big-note">'.format(note_image)
                                        * (difficulty_level // 5)),
                            small_images=(u'<img src="{}" class="song-small-note">'.format(note_image)
                                          * (difficulty_level % 5)),
                            notes=_(u'{} notes').format(notes),
                        )),
                        'image': u'{static_url}img/songs/{difficulty}.png'.format(
                            static_url=RAW_CONTEXT['static_url'],
                            difficulty=difficulty,
                        ),
                    }

            if 'played' in fields:
                setSubField(fields, 'played', key='link', value=u'{}&view=leaderboard&ordering=score&reverse_order=on'.format(fields['played']['link']))
                setSubField(fields, 'played', key='ajax_link', value=u'{}&view=leaderboard&ordering=score&reverse_order=on&ajax_modal_only'.format(fields['played']['ajax_link']))

            details = u''
            for fieldName, verbose_name in models.Song.SONGWRITERS_DETAILS:
                value = getattr(item, fieldName)
                if value:
                    details += u'<b>{}</b>: {}<br />'.format(verbose_name, value)
            if details:
                fields['songwriters'] = {
                    'verbose_name': _('Songwriters'),
                    'type': 'html',
                    'value': mark_safe(u'<div class="songwriters-details">{}</div>'.format(details)),
                    'icon': 'id',
                }
            return fields

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']

        def to_translate_form_class(self):
            super(SongCollection.EditView, self).to_translate_form_class()
            self._translate_form_class = forms.to_translate_song_form_class(self._translate_form_class)

############################################################
# Collectible items Collection

COLLECTIBLEITEM_ICON = {
    'quantity': 'scoreup',
}

def to_CollectibleItemCollection(cls):
    class _CollectibleItemCollection(cls):
        title = _('Item')
        plural_title = _('Items')

        class ListView(cls.ListView):
            item_template = 'collectibleitemItem'

        class ItemView(cls.ItemView):
            def to_fields(self, item, extra_fields=None, *args, **kwargs):
                if extra_fields is None: extra_fields = []
                extra_fields.append((
                    'item_details', {
                        'verbose_name': item.item.t_name,
                        'value': item.item.t_description,
                        'type': 'long_text',
                        'icon': 'star',
                    },
                ))
                fields = super(_CollectibleItemCollection.ItemView, self).to_fields(
                    item, *args, icons=COLLECTIBLEITEM_ICON,
                    extra_fields=extra_fields, **kwargs)
                return fields

        class AddView(cls.AddView):
            unique_per_owner = True

    return _CollectibleItemCollection

############################################################
# Items Collection

class ItemCollection(MagiCollection):
    title = _('Item')
    plural_title = _('Items')
    queryset = models.Item.objects.all()
    translated_fields = ('name', 'description', )
    icon = 'star'
    navbar_link = False
    multipart = True
    form_class = forms.ItemForm
    collectible = models.CollectibleItem

    def collectible_to_class(self, model_class):
        cls = super(ItemCollection, self).collectible_to_class(model_class)
        return to_CollectibleItemCollection(cls)

    class ListView(MagiCollection.ListView):
        item_template = custom_item_template
        before_template = 'include/galleryBackButtons'
        per_line = 4

    class ItemView(MagiCollection.ItemView):
        comments_enabled = False

        def to_fields(self, item, *args, **kwargs):
            return OrderedDict([
                ('area_item', {
                    'verbose_name': item.t_name,
                    'value': item.t_description,
                    'type': 'long_text',
                    'icon': 'present',
                }),
            ])

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']

############################################################
# Areas Collection

class AreaCollection(MagiCollection):
    title = _('Area')
    plural_title = _('Areas')
    queryset = models.Area.objects.all()
    translated_fields = ('name', )
    icon = 'world'
    navbar_link = False
    multipart = True
    form_class = forms.AreaForm

    class ListView(MagiCollection.ListView):
        before_template = 'include/beforeAreas'
        after_template = 'include/afterAreas'
        per_line = 3
        item_template = custom_item_template

        def extra_context(self, context):
            super(AreaCollection.ListView, self).extra_context(context)
            context['area_items_sentence'] = _('See all')
            context['gallery_sentence'] = _('Gallery')

    class ItemView(MagiCollection.ItemView):
        enabled = False

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']

############################################################
# Collectible area items Collection

COLLECTIBLEAREAITEM_ICON = {
    'level': 'scoreup',
}

def to_CollectibleAreaItemCollection(cls):
    class _CollectibleAreaItemCollection(cls):
        title = _('Area item')
        plural_title = _('Area items')
        form_class = forms.to_CollectibleAreaItemForm(cls)

        class ListView(cls.ListView):
            item_template = 'collectibleitemItem'

        class ItemView(cls.ItemView):
            def to_fields(self, item, extra_fields=None, *args, **kwargs):
                if extra_fields is None: extra_fields = []
                extra_fields.append((
                    'item_details', {
                        'verbose_name': item.formatted_name,
                        'value': item.formatted_description,
                        'type': 'long_text',
                        'icon': 'present',
                    },
                ))
                fields = super(_CollectibleAreaItemCollection.ItemView, self).to_fields(
                    item, *args, icons=COLLECTIBLEAREAITEM_ICON,
                    extra_fields=extra_fields, **kwargs)
                return fields

        class AddView(cls.AddView):
            unique_per_owner = True
            add_to_collection_variables = cls.AddView.add_to_collection_variables + [
                'type',
            ]

    return _CollectibleAreaItemCollection

############################################################
# Area items Collection

AREA_ITEM_CUTEFORM = {
    'member': {
        'to_cuteform': lambda k, v: FAVORITE_CHARACTERS_IMAGES[k],
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
    'i_attribute': {},
    'i_band': {
        'image_folder': 'band',
        'to_cuteform': 'value',
        'title': _('Band'),
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
}

class AreaItemCollection(MagiCollection):
    title = _('Area item')
    plural_title = _('Area items')
    queryset = models.AreaItem.objects.all()
    translated_fields = ('name', 'instrument', )
    icon = 'present'
    navbar_link = False
    multipart = True
    filter_cuteform = AREA_ITEM_CUTEFORM

    types = {
        _type: {
            'title': _info['translation'],
            'form_class': forms.areaitem_type_to_form(_type),
        }
        for _type, _info in models.AreaItem.TYPES.items()
    }

    collectible = models.CollectibleAreaItem

    def collectible_to_class(self, model_class):
        cls = super(AreaItemCollection, self).collectible_to_class(model_class)
        return to_CollectibleAreaItemCollection(cls)

    class ListView(MagiCollection.ListView):
        filter_form = forms.AreaItemFilters
        ajax_item_popover = True
        before_template = 'include/galleryBackButtons'
        item_template = custom_item_template

        def extra_context(self, context):
            super(AreaItemCollection.ListView, self).extra_context(context)
            context['level_1_sentence'] = _('Level {level}').format(level=1)

    class ItemView(MagiCollection.ItemView):
        comments_enabled = False

        def to_fields(self, item, *args, **kwargs):
            return OrderedDict([
                ('area_item', {
                    'verbose_name': item.formatted_name,
                    'value': item.formatted_description,
                    'type': 'long_text',
                    'icon': 'present',
                }),
            ])

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']

############################################################
# Assets Collection

ASSET_CUTEFORM = {
    'member': {
        'to_cuteform': lambda k, v: FAVORITE_CHARACTERS_IMAGES[k],
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
    'i_band': {
        'image_folder': 'band',
        'to_cuteform': 'value',
        'title': _('Band'),
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
    'i_version': {
        'to_cuteform': lambda k, v: AccountCollection._version_images[k],
        'image_folder': 'language',
        'transform': CuteFormTransform.ImagePath,
    },
    'event': {
        'to_cuteform': lambda k, v: v.image_url,
        'title': _('Event'),
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
}

ASSET_ORDER = ['name', 'type'] + [
    u'{}image'.format(_v['prefix']) for _v in models.Account.VERSIONS.values()
]

ASSET_ICONS = {
    'band': 'users',
    'name': 'album',
    'type': 'toggler',
    'tags': 'star-empty',
}

class AssetCollection(MagiCollection):
    title = _('Asset')
    plural_title = _('Assets')
    queryset = models.Asset.objects.all()
    translated_fields = ('name', )
    icon = 'pictures'
    navbar_link = False
    multipart = True
    filter_cuteform = ASSET_CUTEFORM
    form_class = forms.AssetForm

    types = {
        _type: {
            'title': _info['translation'],
            'form_class': forms.asset_type_to_form(_type),
        }
        for _type, _info in models.Asset.TYPES.items()
    }

    def to_fields(self, view, item, extra_fields=None, exclude_fields=None, order=None, *args, **kwargs):
        if extra_fields is None: extra_fields = []
        if exclude_fields is None: exclude_fields = []
        exclude_fields += ['value']
        if not order:
            order = ASSET_ORDER
        if item.image:
            extra_fields.append(('image', {
                'image': staticImageURL('language/ja.png'),
                'verbose_name': string_concat(_('Japanese version'), ' - ', _('Image')),
                'value': item.image_url,
                'type': 'image',
            }))
        fields = super(AssetCollection, self).to_fields(view, item, *args, icons=ASSET_ICONS, images={
            'image': staticImageURL('language/ja.png'),
            'english_image': staticImageURL('language/world.png'),
            'taiwanese_image': staticImageURL('language/zh-hant.png'),
            'korean_image': staticImageURL('language/kr.png'),
        }, extra_fields=extra_fields, exclude_fields=exclude_fields, order=order, **kwargs)
        setSubField(fields, 'band', key='type', value=lambda f: 'image_link')
        setSubField(fields, 'band', key='link', value=lambda f: u'/members/?i_band={}'.format(item.i_band))
        setSubField(fields, 'band', key='ajax_link', value=lambda f: u'/ajax/members/?i_band={}&ajax_modal_only'.format(item.i_band))
        setSubField(fields, 'band', key='link_text', value=lambda f: item.band)
        setSubField(fields, 'band', key='value', value=lambda f: '{}img/band/{}.png'.format(RAW_CONTEXT['static_url'], item.band))
        return fields

    class ListView(MagiCollection.ListView):
        before_template = 'include/galleryBackButtons'
        filter_form = forms.AssetFilterForm

        def extra_context(self, context):
            super(AssetCollection.ListView, self).extra_context(context)
            type = context['request'].GET.get('i_type', None)
            if type in models.Asset.TYPES:
                per_line = models.Asset.TYPES.get(type, {}).get('per_line', self.per_line)
                if context.get('per_line', None) != per_line:
                    context['per_line'] = per_line
                    context['col_size'] = int(math.ceil(12 / context['per_line']))

    class ItemView(MagiCollection.ItemView):
        comments_enabled = False

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']

COSTUME_CUTEFORM = {
    'card': {
        'to_cuteform': lambda k, v: v.image_url,
        'title': _('Card'),
    },
    'member': {
        'to_cuteform': lambda k, v: (FAVORITE_CHARACTERS_IMAGES[k] if k != forms.CostumeFilterForm.ID_OF_MISC_MEMBERS 
            else staticImageURL('i_misc_member.png')),
        'title': _('Member'),
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
}

class CostumeCollection(MagiCollection):
    queryset = models.Costume.objects.select_related('card', 'member')
    title = _('Costume')
    plural_title = _('Costumes')
    multipart = True
    icon = 'users'
    reportable = False
    blockable = False
    translated_fields = ('name',)
    navbar_link_list = 'girlsbandparty'
    form_class = forms.CostumeForm
    filter_cuteform = COSTUME_CUTEFORM

    def to_fields(self, view, item, extra_fields=None, exclude_fields=None, *args, **kwargs):
        extra_fields = extra_fields or []
        exclude_fields = exclude_fields or []
        # these are all redundant with the viewer + extra field below
        exclude_fields.extend(['i_costume_type', 'preview_image', 'model_pkg', 'name'])

        if item.card:
            extra_fields.append(('card', {
                'verbose_name': _('Card'),
                'type': 'text_with_link',
                'value': unicode(item.card),
                'ajax_link': item.card.ajax_item_url,
                'link': item.card.item_url,
                'link_text': _('Open card'),
                'icon': 'album',
                'image': item.card.image_trained_url or item.card.image_url,
            }))
        else:
            member_field_params = {
                'verbose_name': _('Costume'),
                'type': 'text',
                'value': unicode(item.t_name),
                'icon': 'profile',
            }
            if item.member:
                member_field_params.update({
                    'type': 'text_with_link',
                    'ajax_link': item.member.ajax_item_url,
                    'link': item.member.item_url,
                    'link_text': unicode(item.member),
                    'image': item.member.square_image_url,
                })
            extra_fields.append(('costume', member_field_params))
        
        fields = super(CostumeCollection, self).to_fields(view, item, extra_fields=extra_fields, exclude_fields=exclude_fields, *args, **kwargs)
        return fields
    
    def buttons_per_item(self, view, request, context, item):
        buttons = super(CostumeCollection, self).buttons_per_item(view, request, context, item)

        # Card-associated costumes take their name from the card, so you can't translate them.
        if 'translate' in buttons and item.card:
            del buttons['translate']
        
        return buttons

    class ListView(MagiCollection.ListView):
        item_template = custom_item_template
        per_line = 4
        filter_form = forms.CostumeFilterForm
        default_ordering = '-id'
        # not with 4 to a row
        show_relevant_fields_on_ordering = False

        def to_fields(self, item, *args, **kwargs):
            fields = super(CostumeCollection.ListView, self).to_fields(item, *args, **kwargs)
            return fields

    class ItemView(MagiCollection.ItemView):
        top_illustration = 'include/costumeTopIllustration'
        js_files = LIVE2D_JS_FILES
        ajax_callback = 'loadModelViewerAjax'
        show_item_buttons = False
        item_padding = 0

        def extra_context(self, context):
            # the old modal JS loading workaround
            if context['request'].path_info.startswith('/ajax/'):
                is_ajax = True
                context['late_js_files'] = context['js_files']
                context['js_files'] = []
                context['danger_zone'] = 220
            else:
                is_ajax = False
                context['danger_zone'] = 100
            
            if context['request'].GET.get('from_card') is not None:
                # try to simulate the big back link in the previous live2d page
                # only the actual link can be clicked though, unfortunately
                setSubField(context['item_fields'], 'card', key='icon', value='back')

            if not is_ajax:
                # disable AJAX on standalone viewer pages, as having two viewers open at once will cause trouble
                setSubField(context['item_fields'], 'card', key='ajax_link', value=None)
                setSubField(context['item_fields'], 'costume', key='ajax_link', value=None)

            return context

        def get_queryset(self, queryset, parameters, request):
            queryset = super(CostumeCollection.ItemView, self).get_queryset(queryset, parameters, request)
            queryset = queryset.select_related('card').select_related('member')
            return queryset

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']
