# -*- coding: utf-8 -*-
import math
from itertools import chain
from collections import OrderedDict
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.utils.formats import dateformat
from django.utils.safestring import mark_safe
from django.db.models import Prefetch
from magi.magicollections import MagiCollection, AccountCollection as _AccountCollection, ActivityCollection as _ActivityCollection, BadgeCollection as _BadgeCollection, DonateCollection as _DonateCollection, UserCollection as _UserCollection
from magi.utils import setSubField, CuteFormType, CuteFormTransform, FAVORITE_CHARACTERS_IMAGES, getMagiCollection, torfc2822, custom_item_template, staticImageURL
from magi.default_settings import RAW_CONTEXT
from magi.models import Activity
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
            if not context['request'].user.is_authenticated() or not context['request'].user.is_staff:
                context['afterjs'] = context['afterjs'].replace('loadCollectionForOwner(\'/ajax/favoritecards/\', loadCardInList)', 'loadProfileComingSoon')

############################################################
# Account Collection

class AccountCollection(_AccountCollection):
    form_class = forms.AccountForm
    navbar_link_list = 'community'

    _attributes_images = [_c[0] for _c in settings.USER_COLORS]
    _version_images = [_c['image'] for _c in models.Account.VERSIONS.values()]
    _play_with_icons = [_c['icon'] for _c in models.Account.PLAY_WITH.values()]
    filter_cuteform = {
        'member_id': {
            'to_cuteform': lambda k, v: FAVORITE_CHARACTERS_IMAGES[k],
            'extra_settings': {
	        'modal': 'true',
	        'modal-text': 'true',
            },
        },
        'i_attribute': {
            'to_cuteform': lambda k, v: AccountCollection._attributes_images.index(k) + 1,
            'transform': CuteFormTransform.ImagePath,
        },
        'has_friend_id': {
            'type': CuteFormType.OnlyNone,
        },
        'center': {
            'to_cuteform': lambda k, v: v.image_url,
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

    def to_fields(self, view, item, *args, **kwargs):
        fields = super(AccountCollection, self).to_fields(view, item, *args, icons={
            'play_with': item.play_with_icon,
            'os': item.os_icon,
            'device': item.os_icon or 'id',
        }, images={
            'version': item.version_image_url,
            'stargems_bought': staticImageURL(u'stargems_bought.png'),
        }, **kwargs)
        setSubField(fields, 'stargems_bought', key='verbose_name', value=_('Total {item} bought').format(item=_('Star gems').lower()))
        setSubField(fields, 'stargems_bought', key='type', value='text_annotation')
        spent_yen = int(item.stargems_bought * django_settings.PRICE_PER_STARGEM) if item.stargems_bought else 0
        spent_dollars = int(spent_yen * django_settings.YEN_TO_USD)
        setSubField(fields, 'stargems_bought', key='annotation', value=_(u'~{}円 spent (~${})').format(spent_yen, spent_dollars))
        return fields

    def get_profile_account_tabs(self, request, context, *args, **kwargs):
        tabs = super(AccountCollection, self).get_profile_account_tabs(request, context, *args, **kwargs)
        if not request.user.is_authenticated() or not request.user.is_staff:
            for collection_name, collection in context['collectible_collections']['account'].items():
                if collection_name in tabs and collection.add_view.staff_required:
                    tabs[collection_name]['callback'] = 'loadAccountComingSoon'
        return tabs

    def share_image(self, context, item):
        return 'screenshots/leaderboard.png'

    class ListView(_AccountCollection.ListView):
        filter_form = forms.FilterAccounts
        default_ordering = '-level'

    class AddView(_AccountCollection.AddView):
        back_to_list_button = False
        simpler_form = forms.AddAccountForm

        def redirect_after_add(self, request, item, ajax):
            if not ajax:
                return '/cards/?get_started'
            return super(AccountCollection.AddView, self).redirect_after_add(request, item, ajax)

############################################################
# Badge Collection

class BadgeCollection(_BadgeCollection):
    enabled = True

############################################################
# Donate Collection

class DonateCollection(_DonateCollection):
    enabled = True
    navbar_link_list = 'community'

############################################################
# Activity Collection

class ActivityCollection(_ActivityCollection):
    enabled = False

Activity.collection_name = 'news'

class NewsCollection(_ActivityCollection):
    plural_name = 'news'
    title = _('Staff News')
    plural_title = _('Staff News')
    reportable = False
    queryset = Activity.objects.all()
    navbar_link = True
    navbar_link_list = 'more'

    class ListView(_ActivityCollection.ListView):
        show_title = True
        item_template = 'activityItem'
        shortcut_urls = []

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
    navbar_link_title = _('Characters')
    icon = 'idolized'

    reportable = False

    form_class = forms.MemberForm

    def share_image(self, context, item):
        return 'screenshots/members.png'

    def to_fields(self, view, item, *args, **kwargs):
        fields = super(MemberCollection, self).to_fields(view, item, *args, icons={
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

    class ListView(MagiCollection.ListView):
        item_template = custom_item_template
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

    form_class = forms.CardForm
    reportable = False

    _skill_icons = { _i: _c['icon'] for _i, _c in models.Card.SKILL_TYPES.items() }
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
            'to_cuteform': lambda k, v: CardCollection._skill_icons[k],
            'transform': CuteFormTransform.Flaticon,
        },
        'i_side_skill_type': {
            'to_cuteform': lambda k, v: CardCollection._skill_icons[k],
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

    collectible = [
        models.CollectibleCard,
        models.FavoriteCard,
    ]

    def collectible_to_class(self, model_class):
        cls = super(CardCollection, self).collectible_to_class(model_class)
        if model_class.collection_name == 'favoritecard':
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

                    def extra_context(self, context):
                        context['items'] = [item.card for item in context['items']]

                class AddView(cls.AddView):
                    unique_per_owner = True
                    quick_add_to_collection = True
                    staff_required = True

            return _FavoriteCardCollection

        # CollectedCards
        class _CollectibleCardCollection(cls):
            title = _('Card')
            plural_title = _('Cards')

            filter_cuteform = {
                'max_leveled': {
                    'type': CuteFormType.YesNo,
                },
                'first_episode': {
                    'type': CuteFormType.YesNo,
                },
                'memorial_episode': {
                    'type': CuteFormType.YesNo,
                },
            }

            class form_class(cls.form_class):
                def save(self, commit=True):
                    instance = super(_CollectibleCardCollection.form_class, self).save(commit=False)
                    if instance.card.i_rarity not in models.Card.TRAINABLE_RARITIES:
                        instance.trained = False
                    if commit:
                        instance.save()
                    return instance

            def to_fields(self, view, item, *args, **kwargs):
                fields = super(_CollectibleCardCollection, self).to_fields(view, item, *args, icons={
                    'trained': 'idolized',
                    'max_leveled': 'max-level',
                    'first_episode': 'play',
                    'memorial_episode': 'play',
                }, **kwargs)
                setSubField(fields, 'card', key='value', value=u'#{}'.format(item.card.id))
                return fields

            class AddView(cls.AddView):
                staff_required = True

        return _CollectibleCardCollection

    def share_image(self, context, item):
        return 'screenshots/cards.png'

    def to_fields(self, view, item, *args, **kwargs):
        fields = super(CardCollection, self).to_fields(view, item, *args, icons={
            'rarity': 'star',
            'performance_max': 'skill',
            'performance_trained_max': 'skill',
            'technique_max': 'skill',
            'technique_trained_max': 'skill',
            'visual_max': 'skill',
            'visual_trained_max': 'skill',
            'member': 'idolized',
            'name': 'id',
            'versions': 'world',
        }, images={
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
            buttons['favoritecard']['classes'].remove('staff-only')
        if 'collectiblecard' in buttons:
            buttons['collectiblecard']['classes'].remove('staff-only')
        if view.view == 'list_view' and 'edit' in buttons:
            del(buttons['edit'])
        return buttons

    class ItemView(MagiCollection.ItemView):
        top_illustration = 'items/cardItem'
        ajax_callback = 'loadCard'

        def to_fields(self, item, only_fields=None, *args, **kwargs):
            fields = super(CardCollection.ItemView, self).to_fields(
                item, *args, to_dict=False, only_fields=only_fields, **kwargs)
            new_fields = []
            # Add id field
            new_fields = [('id', {
                'verbose_name': _(u'ID'),
                'type': 'text',
                'value': item.id,
                'icon': 'id',
            })]
            # Add title field
            title = item.japanese_name if item.japanese_name else (item.name if item.name and get_language() != 'ja' else None)
            value = item.name if item.name and get_language() != 'ja' and title != item.name else None
            if title or value:
                new_fields.append(('card_name', {
                    'verbose_name': _('Title'),
                    'type': 'title_text' if title and value else 'text',
                    'title': title,
                    'value': value or title,
                    'icon': 'id',
                }))
            for field in fields:
                field_name = field[0]
                if (not field_name.endswith('_max')
                    and not field_name.endswith('_min')
                    and field_name not in [
                        'name', 'japanese_name', 'skill_name', 'skill_details', 'side_skill_details',
                        'image_trained', 'art', 'art_trained', 'transparent', 'transparent_trained',
                ] and (get_language() != 'ja' or field_name not in [
                    'versions', 'skill_type'
                ])):
                       new_fields.append(field)
                if field_name == 'skill_type': # insert japanese skill after skill
                    new_fields.append(('japanese_skill', {
                        'verbose_name': string_concat(_('Skill'), ' (', t['Japanese'], ')') if get_language() != 'ja' else _('Skill'),
                        'icon': item.skill_icon,
                        'type': 'title_text',
                        'title': item.japanese_skill_type,
                        'value': item.japanese_skill,
                    }))
                if field_name == 'side_skill_type': # insert japanese side skill after side skill
                    new_fields.append(('japanese_side_skill', {
                        'verbose_name': string_concat(_('Side skill'), ' (', t['Japanese'], ')') if get_language() != 'ja' else _('Side skill'),
                        'icon': item.side_skill_icon,
                        'type': 'title_text',
                        'title': item.japanese_side_skill_type,
                        'value': item.japanese_side_skill,
                    }))
            # Add gacha and events
            if item.cached_event:
                new_fields.append(('event', {
                    'verbose_name': u'{}: {}'.format(
                        _('Event'),
                        item.cached_event.japanese_name if get_language() == 'ja' else item.cached_event.name),
                    'icon': 'event',
                    'value': item.cached_event.image_url,
                    'type': 'image_link',
                    'link': item.cached_event.item_url,
                    'ajax_link': item.cached_event.ajax_item_url,
                    'link_text': item.cached_event.japanese_name if get_language() == 'ja' else item.cached_event.name,
                }))
            if item.cached_gacha:
                new_fields.append(('gacha', {
                    'icon': 'max-bond',
                    'verbose_name': u'{}: {}'.format(
                        _('Gacha'),
                        item.cached_gacha.japanese_name if get_language() == 'ja' else item.cached_gacha.name),
                    'value': item.cached_gacha.image_url,
                    'type': 'image_link',
                    'link': item.cached_gacha.item_url,
                    'ajax_link': item.cached_gacha.ajax_item_url,
                    'link_text': item.cached_gacha.japanese_name if get_language() == 'ja' else item.cached_gacha.name,
                }))
            # Add images fields
            for image, verbose_name in [('image', _('Icon')), ('art', _('Art')), ('transparent', _('Transparent'))]:
                if getattr(item, image):
                    new_fields.append((u'{}s'.format(image), {
                        'verbose_name': verbose_name,
                        'type': 'images',
                        'images': [{
                            'value': image_url,
                            'verbose_name': verbose_name,
                        } for image_url in [
                            getattr(item, u'{}_url'.format(image)),
                            getattr(item, u'{}_trained_url'.format(image)),
                        ] if image_url],
                        'icon': 'pictures',
                    }))
            # Add chibis
            if item.cached_chibis:
                new_fields.append(('chibis', {
                    'icon': 'pictures',
                    'type': 'images',
                    'verbose_name': _('Chibi'),
                    'images': [{
                        'value': chibi.image_url,
                        'verbose_name': _('Chibi'),
                    } for chibi in item.cached_chibis],
                }))
            fields = OrderedDict(new_fields)
            # Modify existing fields
            # skill name
            setSubField(fields, 'japanese_skill_name', key='verbose_name', value=_('Skill name'))
            setSubField(fields, 'japanese_skill_name', key='icon', value='skill')
            if item.skill_name:
                setSubField(fields, 'japanese_skill_name', key='type', value='title_text')
                setSubField(fields, 'japanese_skill_name', key='title', value=item.japanese_skill_name)
                setSubField(fields, 'japanese_skill_name', key='value', value=item.skill_name)
            # skill details
            setSubField(fields, 'skill_type', key='type', value='title_text')
            setSubField(fields, 'skill_type', key='title', value=item.t_skill_type)
            setSubField(fields, 'skill_type', key='value', value=item.skill)
            setSubField(fields, 'skill_type', key='icon', value=lambda k: item.skill_icon)
            # side skill details
            setSubField(fields, 'side_skill_type', key='type', value='title_text')
            setSubField(fields, 'side_skill_type', key='title', value=item.t_side_skill_type)
            setSubField(fields, 'side_skill_type', key='value', value=item.side_skill)
            setSubField(fields, 'side_skill_type', key='icon', value=lambda k: item.side_skill_icon)
            return fields

    class ListView(MagiCollection.ListView):
        item_template = custom_item_template
        per_line = 2
        page_size = 36
        filter_form = forms.CardFilterForm
        default_ordering = '-id'
        ajax_pagination_callback = 'loadCardInList'

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
                for item in context['items']:
                    item.show_item_buttons_as_icons = True
            return context

        def to_fields(self, item, only_fields=None, *args, **kwargs):
            fields = super(CardCollection.ListView, self).to_fields(item, *args, only_fields=only_fields, **kwargs)
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

    class AddView(MagiCollection.AddView):
        staff_required = True
        multipart = True

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True

class EventCollection(MagiCollection):
    queryset = models.Event.objects.all()
    title = _('Event')
    plural_title = _('Events')
    icon = 'event'
    form_class = forms.EventForm
    multipart = True
    reportable = False
    navbar_link_list = 'events'

    filter_cuteform = {
        'main_card': {
            'to_cuteform': lambda k, v: v.image_url,
            'extra_settings': {
	        'modal': 'true',
	        'modal-text': 'true',
            },
        },
        'secondary_card': {
            'to_cuteform': lambda k, v: v.image_url,
            'extra_settings': {
	        'modal': 'true',
	        'modal-text': 'true',
            },
        },
        'i_boost_attribute': {
            'image_folder': 'i_attribute',
        },
    }

    collectible = models.EventParticipation

    def collectible_to_class(self, model_class):
        cls = super(EventCollection, self).collectible_to_class(model_class)
        if model_class.collection_name == 'eventparticipation':

            class _EventParticipationCollection(cls):
                title = _('Participated event')
                plural_title = _('Participated events')

                class form_class(cls.form_class):
                    class Meta(cls.form_class.Meta):
                        optional_fields = ('score', 'ranking', 'song_score', 'song_ranking')

                def to_fields(self, view, item, *args, **kwargs):
                    return super(_EventParticipationCollection, self).to_fields(view, item, *args, icons={
                        'score': 'scoreup',
                        'ranking': 'trophy',
                        'song_score': 'song',
                        'song_ranking': 'trophy'
                    }, **kwargs)

                class ListView(cls.ListView):
                    per_line = 3

                class AddView(cls.AddView):
                    staff_required = True

            return _EventParticipationCollection
        return cls


    def to_fields(self, view, item, *args, **kwargs):
        fields = super(EventCollection, self).to_fields(view, item, *args, icons={
            'name': 'world',
            'japanese_name': 'JP',
            'start_date': 'date',
            'end_date': 'date',
            'rare_stamp': 'max-bond',
            'stamp_translation': 'max-bond',
        }, images={
            'boost_attribute': u'{static_url}img/i_attribute/{value}.png'.format(
                static_url=RAW_CONTEXT['static_url'],
                value=item.i_boost_attribute,
            ),
        }, **kwargs)
        if get_language() == 'ja' and 'name' in fields and 'japanese_name' in fields:
            setSubField(fields, 'japanese_name', key='verbose_name', value=fields['name']['verbose_name'])
            del(fields['name'])
        if item.name == item.japanese_name and 'japanese_name' in fields:
            del(fields['japanese_name'])
        setSubField(fields, 'start_date', key='timezones', value=['Asia/Tokyo', 'Local time'])
        setSubField(fields, 'end_date', key='timezones', value=['Asia/Tokyo', 'Local time'])
        return fields

    class ListView(MagiCollection.ListView):
        per_line = 2
        default_ordering = '-start_date'
        hide_sidebar = True
        filter_form = forms.EventFilterForm
        show_collect_button = {
            'eventparticipation': False,
        }

    class ItemView(MagiCollection.ItemView):
        template = 'default'

        def get_queryset(self, queryset, parameters, request):
            queryset = super(EventCollection.ItemView, self).get_queryset(queryset, parameters, request)
            queryset = queryset.select_related('main_card', 'secondary_card').prefetch_related(Prefetch('boost_members', to_attr='all_members'), Prefetch('gachas', to_attr='all_gachas'), Prefetch('gift_songs', to_attr='all_gifted_songs'))
            return queryset

        def buttons_per_item(self, *args, **kwargs):
            buttons = super(EventCollection.ItemView, self).buttons_per_item(*args, **kwargs)
            if 'eventparticipation' in buttons:
                buttons['eventparticipation']['classes'].remove('staff-only')
            return buttons

        def to_fields(self, item, *args, **kwargs):
            fields = super(EventCollection.ItemView, self).to_fields(item, *args, to_dict=False, **kwargs)
            if item.status and item.status != 'ended':
                fields.insert(0, ('countdown', {
                    'verbose_name': _('Countdown'),
                    'value': mark_safe(u'<span class="fontx1-5 countdown" data-date="{date}" data-format="{sentence}"></h4>').format(
                        date=torfc2822(item.end_date if item.status == 'current' else item.start_date),
                        sentence=_('{time} left') if item.status == 'current' else _('Starts in {time}'),
                    ),
                    'icon': 'times',
                    'type': 'html',
                }))
            fields = OrderedDict(fields)
            if len(item.all_gachas):
                fields['gacha'] = {
                    'icon': 'max-bond',
                    'verbose_name': _('Gacha'),
                    'type': 'images_links',
                    'images': [{
                        'value': gacha.image_url,
                        'link': gacha.item_url,
                        'ajax_link': gacha.ajax_item_url,
                        'link_text': unicode(gacha),
                    } for gacha in item.all_gachas]
                }
            if len(item.all_members):
                fields['boost_members'] = {
                    'icon': 'users',
                    'verbose_name': _('Boost Members'),
                    'type': 'images_links',
                    'images': [{
                        'value': member.square_image_url,
                        'link': member.item_url,
                        'ajax_link': member.ajax_item_url,
                        'link_text': unicode(member),
                    } for member in item.all_members]
                }
            if item.main_card_id or item.secondary_card_id:
                fields['cards'] = {
                    'icon': 'cards',
                    'verbose_name': _('Cards'),
                    'type': 'images_links',
                    'images': [{
                        'value': card.image_url,
                        'link': card.item_url,
                        'ajax_link': card.ajax_item_url,
                        'link_text': unicode(card),
                    } for card in [item.main_card, item.secondary_card] if card is not None]
                }
            if len(item.all_gifted_songs):
                fields['songs'] = {
                    'icon': 'song',
                    'verbose_name': _('Gift song'),
                    'type': 'images_links',
                    'images': [{
                        'value': gifted_song.image_url,
                        'link': gifted_song.item_url,
                        'ajax_link': gifted_song.ajax_item_url,
                        'link_text': unicode(gifted_song),
                    } for gifted_song in item.all_gifted_songs]
                }
            return fields


    class AddView(MagiCollection.AddView):
        staff_required = True
        savem2m = True

    class EditView(MagiCollection.EditView):
        staff_required = True
        savem2m = True

class GachaCollection(MagiCollection):
    queryset = models.Gacha.objects.all()
    icon = 'max-bond'
    title = _('Gacha')
    plural_title = _('Gacha')
    form_class = forms.GachaForm
    multipart = True
    navbar_link_list = 'events'
    reportable = False

    filter_cuteform = {
        'i_attribute': {},
        'event': {
            'to_cuteform': lambda k, v: v.image_url,
            'extra_settings': {
	        'modal': 'true',
	        'modal-text': 'true',
            },
        },
    }

    def to_fields(self, view, item, in_list=False, *args, **kwargs):
        fields = super(GachaCollection, self).to_fields(view, item, *args, icons={
            'name': 'max-bond',
            'japanese_name': 'max-bond',
            'start_date': 'date',
            'end_date': 'date',
            'event': 'event',
        }, images={
            'attribute': u'{static_url}img/i_attribute/{value}.png'.format(
                static_url=RAW_CONTEXT['static_url'],
                value=item.i_attribute,
            ),
        }, **kwargs)
        if get_language() == 'ja':
            setSubField(fields, 'name', key='value', value=item.japanese_name)
        else:
            setSubField(fields, 'name', key='type', value='title_text')
            setSubField(fields, 'name', key='title', value=item.name)
            setSubField(fields, 'name', key='value', value=item.japanese_name)
        setSubField(fields, 'start_date', key='timezones', value=['Asia/Tokyo', 'Local time'])
        setSubField(fields, 'end_date', key='timezones', value=['Asia/Tokyo', 'Local time'])
        setSubField(fields, 'event', key='type', value='image_link')
        setSubField(fields, 'event', key='value', value=lambda f: item.event.image_url)
        setSubField(fields, 'event', key='link_text', value=lambda f: item.event.japanese_name if get_language() == 'ja' else item.event.name)
        return fields

    class ItemView(MagiCollection.ItemView):
        template = 'default'

        def get_queryset(self, queryset, parameters, request):
            queryset = super(GachaCollection.ItemView, self).get_queryset(queryset, parameters, request)
            queryset = queryset.select_related('event').prefetch_related(Prefetch('cards', to_attr='all_cards'))
            return queryset

        def to_fields(self, item, in_list=False, *args, **kwargs):
            fields = super(GachaCollection.ItemView, self).to_fields(item, *args, to_dict=False, **kwargs)
            if item.status and item.status != 'ended':
                fields.insert(0, ('countdown', {
                    'verbose_name': _('Countdown'),
                    'value': mark_safe(u'<span class="fontx1-5 countdown" data-date="{date}" data-format="{sentence}"></h4>').format(
                        date=torfc2822(item.end_date if item.status == 'current' else item.start_date),
                        sentence=_('{time} left') if item.status == 'current' else _('Starts in {time}'),
                    ),
                    'icon': 'times',
                    'type': 'html',
                }))
            fields = OrderedDict(fields)
            if 'japanese_name' in fields:
                del(fields['japanese_name'])
            if len(item.all_cards):
                fields['cards'] = {
                    'icon': 'cards',
                    'verbose_name': _('Cards'),
                    'type': 'images_links',
                    'images': [{
                        'value': card.image_url,
                        'link': card.item_url,
                        'ajax_link': card.ajax_item_url,
                        'link_text': unicode(card),
                    } for card in item.all_cards],
                }
            return fields

    class ListView(MagiCollection.ListView):
        default_ordering = '-start_date'
        per_line = 2

    def _after_save(self, request, instance):
        for card in instance.cards.all():
            card.update_cache_gacha()
        return instance

    class AddView(MagiCollection.AddView):
        savem2m = True
        staff_required = True

        def after_save(self, request, instance, type=None):
            return self.collection._after_save(request, instance)

    class EditView(MagiCollection.EditView):
        savem2m = True
        staff_required = True

        def after_save(self, request, instance):
            return self.collection._after_save(request, instance)

############################################################
# Songs Collection

_song_cuteform = {
    'i_band': {
        'image_folder': 'band',
        'to_cuteform': 'value',
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
    'event': {
        'to_cuteform': lambda k, v: v.image_url,
        'extra_settings': {
	    'modal': 'true',
	    'modal-text': 'true',
        },
    },
}

class SongCollection(MagiCollection):
    queryset = models.Song.objects.all()
    multipart = True
    icon = 'song'
    reportable = False

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
            class _PlayedSongCollection(cls):
                title = _('Played song')
                plural_title = _('Played songs')

                filter_cuteform = dict(_song_cuteform.items() + [
                    ('full_combo', {
                        'type': CuteFormType.YesNo,
                    }),
                    ('i_difficulty', {
                        'to_cuteform': lambda k, v: models.PlayedSong.DIFFICULTY_CHOICES[k][0],
                        'image_folder': 'songs',
                        'transform': CuteFormTransform.ImagePath,
                    }),
                ])

                def to_fields(self, view, item, *args, **kwargs):
                    fields = super(_PlayedSongCollection, self).to_fields(view, item, *args, icons={
                        'score': 'scoreup',
                        'full_combo': 'combo',
                    }, images={
                        'difficulty':  u'{static_url}img/songs/{difficulty}.png'.format(
                            static_url=RAW_CONTEXT['static_url'],
                            difficulty=item.difficulty,
                        ),
                    }, **kwargs)
                    setSubField(fields, 'difficulty', key='value', value=item.t_difficulty)
                    return fields

                class AddView(cls.AddView):
                    staff_required = True

            return _PlayedSongCollection
        return cls

    def to_fields(self, view, item, *args, **kwargs):
        fields = super(SongCollection, self).to_fields(
            view, item, *args, icons={
                'japanese_name': 'song',
                'name': 'world',
                'romaji_name': 'song',
                'itunes_id': 'play',
                'length': 'times',
                'unlock': 'perfectlock',
                'bpm': 'hp',
                'release_date': 'date',
                'event': 'event',
            }, **kwargs)
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

        def buttons_per_item(self, *args, **kwargs):
            buttons = super(SongCollection.ItemView, self).buttons_per_item(*args, **kwargs)
            if 'playedsong' in buttons:
                buttons['playedsong']['classes'].remove('staff-only')
            return buttons

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

    class EditView(MagiCollection.EditView):
        staff_required = True
