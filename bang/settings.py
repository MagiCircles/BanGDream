# -*- coding: utf-8 -*-
import datetime, pytz
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _
from web.default_settings import DEFAULT_ENABLED_PAGES
from web.utils import tourldash
from bang import models

SITE_NAME = 'Bandori Party'
SITE_URL = 'http://bandori.party/'
SITE_IMAGE = 'bandori_party.png'
SITE_LOGO = 'bandori_party_logo.png'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.bandori.party/'

LAUNCH_DATE = datetime.datetime(2017, 04, 9, 12, 0, 0, tzinfo=pytz.UTC)

SITE_LOGO_PER_LANGUAGE = {
    'ja': 'bandori_party_logo_japanese.png',
}

GAME_NAME = _('BanG Dream! Girls Band Party')
GAME_URL = 'https://bang-dream.bushimo.jp/'

DISQUS_SHORTNAME = 'bangdream'
ACCOUNT_MODEL = models.Account
COLOR = '#E40046'

GITHUB_REPOSITORY = ('SchoolIdolTomodachi', 'BanGDream')

CONTACT_EMAIL = 'contact@bandori.party'
CONTACT_REDDIT = 'AmbiBambiii'
CONTACT_FACEBOOK = 'TheViolentAliceSyndrome'

TWITTER_HANDLE = 'BandoriParty'
HASHTAGS = [u'バンドリ', u'ガルパ']

ABOUT_PHOTO = 'deby.jpg'

EMPTY_IMAGE = 'stars_with_white.png'

SITE_NAV_LOGO = 'stars.png'

FAVORITE_CHARACTERS = django_settings.FAVORITE_CHARACTERS
FAVORITE_CHARACTER_TO_URL = lambda link: '/member/{pk}/{name}/'.format(pk=link.raw_value, name=tourldash(link.value))
FAVORITE_CHARACTER_NAME = _(u'{nth} Favorite Member')

ACTIVITY_TAGS = [
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

STATIC_FILES_VERSION = '1'

ENABLED_PAGES = DEFAULT_ENABLED_PAGES
ENABLED_PAGES['index']['enabled'] = True
ENABLED_PAGES['index']['custom'] = True
