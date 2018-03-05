# -*- coding: utf-8 -*-
import datetime, pytz
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _, string_concat

from magi.default_settings import DEFAULT_ENABLED_NAVBAR_LISTS, DEFAULT_ENABLED_PAGES, DEFAULT_NAVBAR_ORDERING, DEFAULT_JAVASCRIPT_TRANSLATED_TERMS
from magi.utils import tourldash
from bang import models

STATIC_FILES_VERSION = django_settings.STATIC_FILES_VERSION

SITE_NAME = 'Bandori Party'
SITE_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//bandori.party/'
SITE_IMAGE = 'bandori_party.png'
SITE_LOGO = 'bandori_party_logo.png'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.bandori.party/'

LAUNCH_DATE = datetime.datetime(2017, 04, 9, 12, 0, 0, tzinfo=pytz.UTC)

SITE_LOGO_PER_LANGUAGE = {
    'ja': 'bandori_japanese.png',
    'tw': 'bandori_taiwanese.png',
    'kr': 'bandori_korean.png',
    'ru': 'bandori_russian.png',
}

GAME_NAME = string_concat(_('BanG Dream!'), ' ', _('Girls Band Party'))
GAME_URL = 'https://bang-dream.bushimo.jp/'

DISQUS_SHORTNAME = 'bangdream'
ACCOUNT_MODEL = models.Account
COLOR = '#E40046'

GITHUB_REPOSITORY = ('SchoolIdolTomodachi', 'BanGDream')

CONTACT_EMAIL = 'contact@bandori.party'
CONTACT_REDDIT = 'AmbiBambiii'
CONTACT_FACEBOOK = 'BandoriParty'
FEEDBACK_FORM = 'https://docs.google.com/forms/d/1lfd3x4TX6R1IYrZqhwPN_GqghCQpBLwNkkwro7uBAxI/viewform'

TWITTER_HANDLE = 'BandoriParty'
HASHTAGS = [u'バンドリ', u'ガルパ']

FIRST_COLLECTION = 'collectiblecard'
GET_STARTED_VIDEO = 'TqL9nSNouhw'

ABOUT_PHOTO = 'deby.jpg'

EMPTY_IMAGE = 'stars_with_white.png'

SITE_NAV_LOGO = 'star.png'

FAVORITE_CHARACTERS = django_settings.FAVORITE_CHARACTERS
FAVORITE_CHARACTER_TO_URL = lambda link: '/member/{pk}/{name}/'.format(pk=link.raw_value, name=tourldash(link.value))
FAVORITE_CHARACTER_NAME = _(u'{nth} Favorite Member')

_ACTIVITY_TAGS = [
    ('comedy', _('Comedy')),
    ('cards', _('New Cards')),
    ('event', _('Event')),
    ('live', _('Live')),
    ('introduction', _('Introduce yourself')),
    ('members', _('Members')),
    ('anime', _('Anime')),
    ('cosplay', _('Cosplay')),
    ('fanart', _('Fan made')),
    ('merch', _('Merchandise')),
    ('community', _('Community')),
    ('unrelated', _('Unrelated')),
]

USER_COLORS = [
    ('power', _('Power'), 'Power', '#FF2D54'),
    ('cool', _('Cool'), 'Cool', '#4057E3'),
    ('pure', _('Pure'), 'Pure', '#44C527'),
    ('happy', _('Happy'), 'Happy', '#FF8400'),
]

GOOGLE_ANALYTICS = 'UA-96550529-1'

ENABLED_PAGES = DEFAULT_ENABLED_PAGES

ENABLED_PAGES['wiki'][0]['enabled'] = True
ENABLED_PAGES['wiki'][1]['enabled'] = True
ENABLED_PAGES['wiki'][0]['divider_before'] = True
ENABLED_PAGES['wiki'][1]['divider_before'] = True
ENABLED_PAGES['wiki'][0]['navbar_link_list'] = 'girlsbandparty'

ENABLED_PAGES['index']['enabled'] = True
ENABLED_PAGES['index']['custom'] = True

ENABLED_PAGES['discord'] = {
    'title': 'Discord',
    'icon': 'comments',
    'navbar_link_list': 'community',
}

ENABLED_PAGES['twitter'] = {
    'title': 'Twitter',
    'icon': 'activities',
    'navbar_link_list': 'community',
}

ENABLED_PAGES['teambuilder'] = {
    'title': _('Team builder'),
    'icon': 'settings',
    'navbar_link': False,
    #'navbar_link_list': 'girlsbandparty',
}

ENABLED_NAVBAR_LISTS = DEFAULT_ENABLED_NAVBAR_LISTS
ENABLED_NAVBAR_LISTS['bangdream'] = {
    'title': _('BanG Dream!'),
    'image': 'BanGDream',
    'order': ['member_list', 'song_list'],
}
ENABLED_NAVBAR_LISTS['girlsbandparty'] = {
    'title': _('Girls Band Party'),
    'image': 'GirlsBandParty',
    'order': ['card_list', 'event_list', 'gacha_list', 'wiki', 'teambuilder'],
}
ENABLED_NAVBAR_LISTS['community'] = {
    'title': _('Community'),
    'icon': 'users',
    'order': ['account_list', 'donate_list', 'discord', 'twitter'],
}

ACCOUNT_TAB_ORDERING = ['collectiblecard', 'eventparticipation', 'playedsong', 'about']

NAVBAR_ORDERING = ['card_list', 'member_list', 'song_list', 'events', 'community'] + DEFAULT_NAVBAR_ORDERING

TOTAL_DONATORS = django_settings.TOTAL_DONATORS
LATEST_NEWS = django_settings.LATEST_NEWS
STAFF_CONFIGURATIONS = django_settings.STAFF_CONFIGURATIONS

JAVASCRIPT_TRANSLATED_TERMS = DEFAULT_JAVASCRIPT_TRANSLATED_TERMS + [
    u'Coming soon',
]
