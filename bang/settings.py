# -*- coding: utf-8 -*-
import datetime
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _, string_concat
from django.utils import timezone

from magi.default_settings import (
    DEFAULT_ENABLED_NAVBAR_LISTS,
    DEFAULT_ENABLED_PAGES,
    DEFAULT_NAVBAR_ORDERING,
    DEFAULT_JAVASCRIPT_TRANSLATED_TERMS,
    DEFAULT_GLOBAL_OUTSIDE_PERMISSIONS,
    DEFAULT_LANGUAGES_CANT_SPEAK_ENGLISH,
    DEFAULT_EXTRA_PREFERENCES,
    DEFAULT_HOME_ACTIVITY_TABS,
)
from magi.utils import tourldash
from bang.utils import bangGlobalContext, randomArtForCharacter
from bang import models

############################################################
# License, game and site settings

SITE_NAME = 'Bandori Party'
SITE_EMOJIS = [u'★', u'🎸', u'🤘']
SITE_IMAGE = 'share/bandori_party.png'
SITE_LOGO = 'logo/bandori_party.png'

GAME_NAME = string_concat(_('BanG Dream!'), ' ', _('Girls Band Party'))
GAME_URL = 'https://bang-dream.bushimo.jp/'

COLOR = '#E40046'

############################################################
# Images

CORNER_POPUP_IMAGE = 'chibi_kanae.png'
ABOUT_PHOTO = 'deby.jpg'
EMPTY_IMAGE = 'stars_with_white.png'
SITE_NAV_LOGO = 'star.png'

############################################################
# Settings per languages

SITE_NAME_PER_LANGUAGE = {
    'ja': u'バンドリパーティー',
    'zh-hans': u'Bandori 派对',
    'zh-hant': u'Bandori 派對',
    'kr' : u'밴드리파티',
    'ru': u'бандори парти',
}

SITE_LOGO_PER_LANGUAGE = {
    'ja': 'logo/bandori_party_japanese.png',
    'zh-hans': 'logo/bandori_party_chinese.png',
    'zh-hant': 'logo/bandori_party_taiwanese.png',
    'kr': 'logo/bandori_party_korean.png',
    'ru': 'logo/bandori_party_russian.png',
}

SITE_IMAGE_PER_LANGUAGE = {
    'en': 'share/bandori_party_english.png',
    'ja': 'share/bandori_party_japanese.png',
    'zh-hans': 'share/bandori_party_chinese.png',
    'zh-hant': 'share/bandori_party_taiwanese.png',
    'kr': 'share/bandori_party_korean.png',
    'ru': 'share/bandori_party_russian.png',
}

############################################################
# Contact & Social

CONTACT_EMAIL = 'contact@bandori.party'
CONTACT_REDDIT = 'AmbiBambiii'
CONTACT_FACEBOOK = 'BandoriParty'
CONTACT_DISCORD = 'https://discord.gg/njKRrAg'

FEEDBACK_FORM = 'https://docs.google.com/forms/d/1lfd3x4TX6R1IYrZqhwPN_GqghCQpBLwNkkwro7uBAxI/viewform'
GITHUB_REPOSITORY = ('SchoolIdolTomodachi', 'BanGDream')

TWITTER_HANDLE = 'BandoriParty'
HASHTAGS = [u'バンドリ', u'ガルパ']

############################################################
# Homepage

RANDOM_ART_FOR_CHARACTER = randomArtForCharacter
HOMEPAGE_BACKGROUND = 'bg_pattern.png'
HOMEPAGE_ART_SIDE = 'left'
HOMEPAGE_ART_POSITION = {
    'position': 'center right',
    'size': '150%',
    'y': '40%',
    'x': '100%',
}
HOMEPAGE_ART_GRADIENT = True

HOME_ACTIVITY_TABS = DEFAULT_HOME_ACTIVITY_TABS.copy()
if 'staffpicks' in HOME_ACTIVITY_TABS:
    del(HOME_ACTIVITY_TABS['staffpicks'])
HOME_ACTIVITY_TABS['top_this_week'] = {
    'title': _('TOP'),
    'icon': 'trophy',
    'form_fields': {
        'ordering': '_cache_total_likes,id',
    },
}

############################################################
# First steps

FIRST_COLLECTION = 'collectiblecard'
GET_STARTED_VIDEO = 'TqL9nSNouhw'

############################################################
# Activities

ACTIVITY_TAGS = [
    ('comedy', _('Comedy')),
    ('meme', _('Meme')),
    ('cards', _('Cards')),
    ('scout', _('Scouting')),
    ('event', _('Event')),
    ('live', _('Songs')),
    ('introduction', _('Introduce yourself')),
    ('members', _('Characters')),
    ('birthday', _('Birthday')),
    ('anime', string_concat(_('Anime'), ' / ', _('Manga'))),
    ('cosplay', _('Cosplay')),
    ('fanart', _('Fan made')),
    ('merch', _('Merchandise')),
    ('community', _('Community')),
    ('question', _('Question')),
    ('staff', {
        'translation': _('Staff picks'),
        'has_permission_to_add': lambda r: r.user.is_staff,
    }),
    ('communityevent', {
        'translation': _('Community event'),
        'has_permission_to_add': lambda r: r.user.hasPermission('post_community_event_activities'),
    }),
    ('pridemonth', {
        'translation': u'PrideMonth🏳️‍🌈',
        'has_permission_to_add': lambda r: timezone.now() < datetime.datetime(2019, 7, 2, 0, tzinfo=timezone.utc),
    }),
    ('petiteidolstudiosummer', {
        'translation': 'PetiteIdolStudioSummer',
        'has_permission_to_add': lambda r: timezone.now() < datetime.datetime(2018, 8, 5, 13, tzinfo=timezone.utc),
    }),
    ('changemymindchallenge', {
        'translation': _('Change My Mind Challenge'),
        'has_permission_to_add': lambda r: timezone.now() < datetime.datetime(2018, 6, 3, tzinfo=timezone.utc),
    }),
    ('thankyouyurushii', {
        'translation': _('Thank you Yurishii'),
        'has_permission_to_add': lambda r: timezone.now() < datetime.datetime(2018, 5, 20, tzinfo=timezone.utc),
    }),
    ('thankyouakesaka', {
        'translation': _('Thank you Ake-san'),
        'has_permission_to_add': lambda r: timezone.now() < datetime.datetime(2018, 9, 25, tzinfo=timezone.utc),
    }),
    ('cosparty18', {
        'translation': _('CosParty 2018'),
        'has_permission_to_add': lambda r: datetime.datetime(2018, 10, 10, 0, tzinfo=timezone.utc) < timezone.now() < datetime.datetime(2018, 11, 15, tzinfo=timezone.utc),
    }),
    ('bandorisnap', {
        'translation': 'Bandori SnaP!',
        'has_permission_to_add': lambda r: datetime.datetime(2019, 10, 2, 13, tzinfo=timezone.utc) < timezone.now() < datetime.datetime(2019, 11, 10, tzinfo=timezone.utc),
    }),
    ('unrelated', lambda: _('Not about {thing}').format(thing=_('BanG Dream!'))),
    ('swearing', _('Swearing')),
    ('nsfw', {
        'translation': _('NSFW'),
        'hidden_by_default': True,
        'has_permission_to_show': lambda r: u'{} {}'.format(_('You need to be over 18 years old.'), _('You can change your birthdate in your settings.') if not r.user.preferences.age else u'') if r.user.is_authenticated() and r.user.preferences.age < 18 else True,
    }),
]

############################################################
# User preferences and profiles

CUSTOM_PREFERENCES_FORM = True

EXTRA_PREFERENCES = DEFAULT_EXTRA_PREFERENCES + [
    ('i_favorite_band', lambda: _('Favorite {thing}').format(thing=_('Band').lower())),
]

FAVORITE_CHARACTER_TO_URL = lambda link: u'/member/{pk}/{name}/'.format(pk=link.raw_value, name=tourldash(link.value))
FAVORITE_CHARACTER_NAME = _('Member')

USER_COLORS = [
    ('power', _('Power'), 'Power', '#FF2D54'),
    ('cool', _('Cool'), 'Cool', '#4057E3'),
    ('pure', _('Pure'), 'Pure', '#44C527'),
    ('happy', _('Happy'), 'Happy', '#FF8400'),
]

ACCOUNT_TAB_ORDERING = ['about', 'collectiblecard', 'eventparticipation', 'playedsong', 'item', 'areaitem']

############################################################
# Staff features

GLOBAL_OUTSIDE_PERMISSIONS = DEFAULT_GLOBAL_OUTSIDE_PERMISSIONS
GLOBAL_OUTSIDE_PERMISSIONS['Google+ Bandori Party group'] = 'https://plus.google.com/communities/118285892680258114918?sqinv=bUtZVFhDQ3BxNWlESTRQUEMwdFdjQTJ2UGc5czd3'

############################################################
# Technical settings

SITE_URL = 'http://localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else 'https://bandori.party/'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.bandori.party/'

GET_GLOBAL_CONTEXT = bangGlobalContext
ACCOUNT_MODEL = models.Account

DISQUS_SHORTNAME = 'bangdream'
GOOGLE_ANALYTICS = 'UA-96550529-1'

JAVASCRIPT_TRANSLATED_TERMS = DEFAULT_JAVASCRIPT_TRANSLATED_TERMS + [
    u'Coming soon',
    u'Open {thing}',
]

############################################################
# From settings or generated_settings

STATIC_FILES_VERSION = django_settings.STATIC_FILES_VERSION
TOTAL_DONATORS = getattr(django_settings, 'TOTAL_DONATORS', None)
LATEST_NEWS = getattr(django_settings, 'LATEST_NEWS', None)
STAFF_CONFIGURATIONS = getattr(django_settings, 'STAFF_CONFIGURATIONS', None)
HOMEPAGE_ARTS = getattr(django_settings, 'HOMEPAGE_ARTS', None)
BACKGROUNDS = getattr(django_settings, 'BACKGROUNDS', None)
FAVORITE_CHARACTERS = getattr(django_settings, 'FAVORITE_CHARACTERS', None)

############################################################
# Customize pages

ENABLED_PAGES = DEFAULT_ENABLED_PAGES

ENABLED_PAGES['wiki'][0]['enabled'] = True
ENABLED_PAGES['wiki'][1]['enabled'] = True
ENABLED_PAGES['wiki'][0]['divider_before'] = True
ENABLED_PAGES['wiki'][0]['navbar_link_list'] = 'girlsbandparty'

ENABLED_PAGES['map']['share_image'] = 'screenshots/map.png'
ENABLED_PAGES['map']['navbar_link_list'] = 'community'

ENABLED_PAGES['settings']['custom'] = True

ENABLED_PAGES['discord'] = {
    'title': 'Discord',
    'icon': 'chat',
    'navbar_link_list': 'community',
    'redirect': 'https://discord.gg/njKRrAg',
    'new_tab': True,
    'check_permissions': lambda c: c['request'].LANGUAGE_CODE not in DEFAULT_LANGUAGES_CANT_SPEAK_ENGLISH,
}

ENABLED_PAGES['twitter'] = {
    'title': 'Twitter',
    'icon': 'twitter',
    'navbar_link_list': 'community',
    'redirect': 'https://twitter.com/bandoriparty',
    'new_tab': True,
    'check_permissions': lambda c: c['request'].LANGUAGE_CODE not in DEFAULT_LANGUAGES_CANT_SPEAK_ENGLISH,
}

ENABLED_PAGES['donate'] = {
    'title': _('Donate'),
    'icon': 'heart',
    'navbar_link_list': 'more',
    'redirect': '/donate/',
}

ENABLED_PAGES['teambuilder'] = {
    'title': _('Team builder'),
    'icon': 'settings',
    'navbar_link': False,
    'authentication_required': True,
    'as_sidebar': True,
    'show_title': True,
    #'navbar_link_list': 'girlsbandparty',
}

ENABLED_PAGES['gallery'] = {
    'title': _('Gallery'),
    'icon': 'pictures',
    'navbar_link_list': 'girlsbandparty',
    'page_description': lambda: u'{} - {}'.format(_('Gallery of {license} images').format(
        license=unicode(GAME_NAME)), u', '.join(
            [unicode(_d['translation']) for _d in models.Asset.TYPES.values()])),
}

ENABLED_PAGES['officialart'] = {
    'title': lambda _c: _('{things} list').format(things=_('Official art')),
    'icon': 'pictures',
    'navbar_link_list': 'bangdream',
    'redirect': '/assets/officialart/',
    'divider_before': True,
}

ENABLED_PAGES['comics'] = {
    'title': lambda _c: _('{things} list').format(things=_('Comics')),
    'icon': 'album',
    'navbar_link_list': 'bangdream',
    'redirect': '/assets/comic/',
}

ENABLED_PAGES['add_rerun'] = {
    'title': u'Add {} rerun dates'.format(u'/'.join(models.Rerun.ITEMS)),
    'staff_required': True,
    'permissions_required': ['manage_main_items'],
    'icon': 'date',
    'navbar_link_list': 'staff',
    'redirect': '/rerun/add/',
}

############################################################
# Customize nav bar

ENABLED_NAVBAR_LISTS = DEFAULT_ENABLED_NAVBAR_LISTS
ENABLED_NAVBAR_LISTS['bangdream'] = {
    'title': _('BanG Dream!'),
    'image': 'BanGDream',
    'order': ['member_list', 'song_list', 'officialart', 'comics'],
}
ENABLED_NAVBAR_LISTS['girlsbandparty'] = {
    'title': _('Girls Band Party'),
    'image': 'GirlsBandParty',
    'order': [
        'card_list', 'cards_quickadd', 'costume_list',
        'event_list', 'gacha_list',
        'item_list', 'area_list',
        'wiki', 'gallery', 'teambuilder',
    ],
}
ENABLED_NAVBAR_LISTS['community'] = {
    'title': _('Community'),
    'icon': 'users',
    'order': ['activity_list', 'account_list', 'map', 'donate_list', 'discord', 'twitter'],
}
ENABLED_NAVBAR_LISTS['more']['order'] = ENABLED_NAVBAR_LISTS['more']['order'] + ['donate']

NAVBAR_ORDERING = ['card_list', 'member_list', 'song_list', 'events', 'community'] + DEFAULT_NAVBAR_ORDERING
