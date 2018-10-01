# -*- coding: utf-8 -*-
from __future__ import division
import datetime, time
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _, pgettext_lazy, string_concat, get_language
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.db import models
from django.conf import settings as django_settings
from magi.models import User, uploadItem
from magi.abstract_models import AccountAsOwnerModel, BaseAccount
from magi.item_model import BaseMagiModel, MagiModel, get_image_url_from_path, get_http_image_url_from_path, i_choices, getInfoFromChoices
from magi.utils import (
    AttrDict,
    tourldash,
    split_data,
    join_data,
    uploadToKeepName,
    staticImageURL,
    FAVORITE_CHARACTERS_NAMES,
    templateVariables,
    uploadTthumb,
    uploadThumb,
    upload2x,
    uploadTiny,
    getEventStatus,
    ColorField,
)
from bang.django_translated import t

############################################################
# Utility Models

LANGUAGES_NEED_OWN_NAME = [ l for l in django_settings.LANGUAGES if l[0] in ['ru', 'zh-hans', 'zh-hant', 'kr'] ]
LANGUAGES_NEED_OWN_NAME_KEYS = [ l[0] for l in django_settings.LANGUAGES if l[0] in ['ru', 'zh-hans', 'zh-hant', 'kr'] ]
LANGUAGES_DIFFERENT_CHARSET = [ l for l in django_settings.LANGUAGES if l[0] in ['ja', 'ru', 'zh-hans', 'zh-hant', 'kr'] ]
LANGUAGES_DIFFERENT_CHARSET_KEYS = [ l[0] for l in django_settings.LANGUAGES if l[0] in ['ja', 'ru', 'zh-hans', 'zh-hant', 'kr'] ]
ALL_ALT_LANGUAGES = [ l for l in django_settings.LANGUAGES if l[0] != 'en' ]
ALL_ALT_LANGUAGES_KEYS = [ l[0] for l in django_settings.LANGUAGES if l[0] != 'en' ]
ALT_LANGUAGES_EXCEPT_JP = [ l for l in django_settings.LANGUAGES if l[0] not in ['en', 'ja'] ]
ALT_LANGUAGES_EXCEPT_JP_KEYS = [ l[0] for l in django_settings.LANGUAGES if l[0] not in ['en', 'ja'] ]

LANGUAGES_TO_VERSIONS = {
    'en': 'EN',
    'es': 'EN',
    'zh-hans': 'TW',
    'ru': 'EN',
    'it': 'EN',
    'fr': 'EN',
    'de': 'EN',
    'pl': 'EN',
    'ja': 'JP',
    'kr': 'KR',
    'id': 'EN',
    'zh-hant': 'TW',
    'pt-br': 'EN',
    'tr': 'EN',
}

VERSIONS_TO_LANGUAGES = {
    'JP': 'ja',
    'EN': 'en',
    'TW': 'zh-hant',
    'KR': 'kr',
}

DREAMFES_PER_LANGUAGE = {
    'ja': u'ドリームフェスティバル',
    'kr': u'드림 페스티벌',
    'zh-hans': u'夢幻祭典轉蛋',
    'zh-hant': u'夢幻祭典轉蛋',
}

############################################################
# Account

class Account(BaseAccount):
    friend_id = models.PositiveIntegerField(_('Friend ID'), null=True)
    center = models.ForeignKey('CollectibleCard', verbose_name=_('Center'), related_name='center_of_account', null=True, on_delete=models.SET_NULL)

    VERSIONS = OrderedDict([
        ('JP', {
            'translation': _('Japanese version'),
            'image': 'ja',
            'prefix': '',
            'code': 'ja',
            'timezone': 'Asia/Tokyo',
        }),
        ('EN', {
            'translation': _('English version'),
            'image': 'world',
            'prefix': 'english_',
            'code': 'en',
            'timezone': 'UTC',
        }),
        ('TW', {
            'translation': _('Taiwanese version'),
            'image': 'zh-hant',
            'prefix': 'taiwanese_',
            'code': 'zh-hant',
            'timezone': 'Asia/Taipei',
        }),
        ('KR', {
            'translation': _('Korean version'),
            'image': 'kr',
            'prefix': 'korean_',
            'code': 'kr',
            'timezone': 'Asia/Seoul',
        }),
    ])
    VERSION_CHOICES = [(_name, _info['translation']) for _name, _info in VERSIONS.items()]
    VERSIONS_PREFIXES = OrderedDict([(_k, _v['prefix']) for _k, _v in VERSIONS.items()])
    i_version = models.PositiveIntegerField(_('Version'), choices=i_choices(VERSION_CHOICES))
    version_image = property(getInfoFromChoices('version', VERSIONS, 'image'))
    version_image_url = property(lambda _a: staticImageURL(_a.version_image, folder=u'language', extension='png'))

    is_playground = models.BooleanField(_('Playground'), default=False, db_index=True)

    PLAY_WITH = OrderedDict([
        ('Thumbs', {
            'translation': _('Thumbs'),
            'icon': 'thumbs'
        }),
        ('Fingers', {
            'translation': _('All fingers'),
            'icon': 'fingers'
        }),
        ('Index', {
            'translation': _('Index fingers'),
            'icon': 'index'
        }),
        ('Hand', {
             'translation': _('One hand'),
            'icon': 'fingers'
        }),
        ('Other', {
            'translation': _('Other'),
            'icon': 'sausage'
        }),
    ])
    PLAY_WITH_CHOICES = [(_name, _info['translation']) for _name, _info in PLAY_WITH.items()]
    i_play_with = models.PositiveIntegerField(_('Play with'), choices=i_choices(PLAY_WITH_CHOICES), null=True)
    play_with_icon = property(getInfoFromChoices('play_with', PLAY_WITH, 'icon'))

    OS_CHOICES = (
        'Android',
        'iOs',
    )
    i_os = models.PositiveIntegerField(_('Operating System'), choices=i_choices(OS_CHOICES), null=True)
    os_icon = property(lambda _a: _a.os.lower() if _a.os else None)

    device = models.CharField(_('Device'), help_text=_('The model of your device. Example: Nexus 5, iPhone 4, iPad 2, ...'), max_length=150, null=True)
    stargems_bought = models.PositiveIntegerField(null=True)

    _thumbnail_screenshot = models.ImageField(null=True, upload_to=uploadThumb('account_screenshot'))
    screenshot = models.ImageField(_('Screenshot'), help_text=_('In-game profile screenshot'), upload_to=uploadItem('account_screenshot'), null=True)
    level_on_screenshot_upload = models.PositiveIntegerField(null=True)
    is_hidden_from_leaderboard = models.BooleanField('Hide from leaderboard', default=False, db_index=True)

    def update_cache_leaderboards(self):
        self._cache_leaderboards_last_update = timezone.now()
        self._cache_leaderboard = type(self).objects.filter(level__gt=self.level, i_version=self.i_version).values('level').distinct().count() + 1

############################################################
# Members

class Member(MagiModel):
    collection_name = 'member'

    owner = models.ForeignKey(User, related_name='added_members')
    name = models.CharField(string_concat(_('Name'), ' (', _('Romaji'), ')'), max_length=100, unique=True)
    japanese_name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100, null=True)

    NAMES_CHOICES = LANGUAGES_NEED_OWN_NAME
    d_names = models.TextField(_('Name'), null=True)

    @property
    def first_name(self):
        if get_language() == 'ja':
            return self.t_name.split(' ')[-1] + u'ちゃん'
        elif get_language() in ['zh-hans', 'zh-hant', 'kr']:
            return self.t_name.split(' ')[-1]
        return self.t_name.split(' ')[0]

    @property
    def t_name(self):
        if get_language() == 'ja':
            return self.japanese_name
        return self.names.get(get_language(), self.name)

    _original_image = models.ImageField(null=True, upload_to=uploadTiny('i'))
    image = models.ImageField(_('Image'), upload_to=uploadItem('i'))
    _original_square_image = models.ImageField(null=True, upload_to=uploadTiny('i/m'))
    square_image = models.ImageField(_('Image'), upload_to=uploadItem('i/m'))

    BAND_CHOICES = (
        'Poppin\'Party',
        'Afterglow',
        'Pastel*Palettes',
        'Roselia',
        'Hello, Happy World!',
    )
    i_band = models.PositiveIntegerField(_('Band'), choices=i_choices(BAND_CHOICES), null=True)
    band_image = lambda _s: staticImageURL(_s.band, folder='band', extension='png')

    school = models.CharField(_('School'), max_length=100, null=True)
    SCHOOLS_CHOICES = ALL_ALT_LANGUAGES
    d_schools = models.TextField(_('School'), null=True)

    SCHOOL_YEAR_CHOICES = (
        ('First', _('First')),
        ('Second', _('Second')),
        ('Third', _('Junior Third')),
    )
    i_school_year = models.PositiveIntegerField(_('School Year'), choices=i_choices(SCHOOL_YEAR_CHOICES), null=True)

    classroom = models.CharField(_('Classroom'), max_length = 10, null=True)

    color = ColorField(_('Color'), null=True, blank=True)

    # TODO: separate page of voice acctresses
    romaji_CV = models.CharField(_('CV'), help_text='In romaji.', max_length=100, null=True)
    CV = models.CharField(string_concat(_('CV'), ' (', t['Japanese'], ')'), help_text='In Japanese characters.', max_length=100, null=True)

    birthday = models.DateField(_('Birthday'), null=True, help_text='The year is not used, so write whatever')

    height = models.PositiveIntegerField(_('Height'), help_text='in cm', null=True)

    food_like = models.CharField(_('Liked food'), max_length=100, null=True)
    FOOD_LIKES_CHOICES = ALL_ALT_LANGUAGES
    d_food_likes = models.TextField(_('Liked food'), null=True)

    food_dislike = models.CharField(_('Disliked food'), max_length=100, null=True)
    FOOD_DISLIKES_CHOICES = ALL_ALT_LANGUAGES
    d_food_dislikes = models.TextField(_('Disliked food'), null=True)

    ASTROLOGICAL_SIGN_CHOICES = (
        ('Leo', _('Leo')),
        ('Aries', _('Aries')),
        ('Libra', _('Libra')),
        ('Virgo', _('Virgo')),
        ('Scorpio', _('Scorpio')),
        ('Capricorn', _('Capricorn')),
        ('Pisces', _('Pisces')),
        ('Gemini', _('Gemini')),
        ('Cancer', _('Cancer')),
        ('Sagittarius', _('Sagittarius')),
        ('Aquarius', _('Aquarius')),
        ('Taurus', _('Taurus')),
    )
    i_astrological_sign = models.PositiveIntegerField(_('Astrological Sign'), choices=i_choices(ASTROLOGICAL_SIGN_CHOICES), null=True)
    @property
    def astrological_sign_image_url(self): return staticImageURL(self.i_astrological_sign, folder='i_astrological_sign', extension='png')

    instrument = models.CharField(_('Instrument'), max_length=100, null=True)
    INSTRUMENTS_CHOICES = ALL_ALT_LANGUAGES
    d_instruments = models.TextField(_('Instrument'), null=True)

    hobbies = models.CharField(_('Hobbies'), max_length=100, null=True)
    HOBBIESS_CHOICES = ALL_ALT_LANGUAGES
    d_hobbiess = models.TextField(_('Hobbies'), null=True)

    description = models.TextField(_('Description'), null=True)
    DESCRIPTIONS_CHOICES = ALL_ALT_LANGUAGES
    d_descriptions = models.TextField(_('Description'), null=True)

    reverse_related = (
        ('cards', 'cards', _('Cards')),
        ('fans', 'users', _('Fans')),
        ('costumes', 'costumes', _('Costumes')),
    )

    # Cache totals
    _cache_totals_days = 1
    _cache_totals_last_update = models.DateTimeField(null=True)
    _cache_total_fans = models.PositiveIntegerField(null=True)
    _cache_total_cards = models.PositiveIntegerField(null=True)
    _cache_total_costumes = models.PositiveIntegerField(null=True)

    def update_cache_totals(self):
        self._cache_totals_last_update = timezone.now()
        self._cache_total_fans = User.objects.filter(
            Q(preferences__favorite_character1=self.id)
            | Q(preferences__favorite_character2=self.id)
            | Q(preferences__favorite_character3=self.id)
        ).count()
        self._cache_total_cards = Card.objects.filter(member=self).count()
        self._cache_total_costumes = Costume.objects.filter(member=self).count()

    def force_cache_totals(self):
        self.update_cache_totals()
        self.save()

    @property
    def cached_total_fans(self):
        if not self._cache_totals_last_update or self._cache_totals_last_update < timezone.now() - datetime.timedelta(hours=self._cache_totals_days):
            self.force_cache_totals()
        return self._cache_total_fans

    @property
    def cached_total_cards(self):
        if not self._cache_totals_last_update or self._cache_totals_last_update < timezone.now() - datetime.timedelta(hours=self._cache_totals_days):
            self.force_cache_totals()
        return self._cache_total_cards

    @property
    def cached_total_costumes(self):
        if not self._cache_totals_last_update or self._cache_totals_last_update < timezone.now() - datetime.timedelta(hours=self._cache_totals_days):
            self.force_cache_totals()
        return self._cache_total_costumes

    def __unicode__(self):
        return unicode(self.t_name)

############################################################
# Card

class Card(MagiModel):
    collection_name = 'card'

    owner = models.ForeignKey(User, related_name='added_cards')
    id = models.PositiveIntegerField(_('ID'), unique=True, primary_key=True, db_index=True)
    member = models.ForeignKey(Member, verbose_name=_('Member'), related_name='cards', null=True, on_delete=models.SET_NULL, db_index=True)

    RARITY_CHOICES = (
        (1, u'★'),
        (2, u'★★'),
        (3, u'★★★'),
        (4, u'★★★★'),
    )
    RARITY_WITHOUT_I_CHOICES = True
    i_rarity = models.PositiveIntegerField(_('Rarity'), choices=RARITY_CHOICES, db_index=True)

    ATTRIBUTES = OrderedDict([
        (1, {
            'translation': _('Power'),
            'english': u'Power',
        }),
        (2, {
            'translation': _('Cool'),
            'english': u'Cool',
        }),
        (3, {
            'translation': _('Pure'),
            'english': u'Pure',
        }),
        (4, {
            'translation': _('Happy'),
            'english': u'Happy',
        }),
    ])
    ATTRIBUTE_CHOICES = [(_name, _info['translation']) for _name, _info in ATTRIBUTES.items()]
    ATTRIBUTE_WITHOUT_I_CHOICES = True
    i_attribute = models.PositiveIntegerField(_('Attribute'), choices=ATTRIBUTE_CHOICES, db_index=True)
    english_attribute = property(getInfoFromChoices('attribute', ATTRIBUTES, 'english'))

    name = models.CharField(_('Title'), max_length=100, null=True)
    NAMES_CHOICES = ALT_LANGUAGES_EXCEPT_JP
    d_names = models.TextField(_('Title'), null=True)
    japanese_name = models.CharField(string_concat(_('Title'), ' (', t['Japanese'], ')'), max_length=100, null=True)

    @property
    def t_name(self):
        if get_language() == 'ja':
            return self.japanese_name or self.name
        return self.names.get(get_language(), self.name or self.japanese_name)

    VERSIONS = Account.VERSIONS
    VERSIONS_CHOICES = Account.VERSION_CHOICES
    c_versions = models.TextField(_('Server availability'), blank=True, null=True, default='"JP"')

    release_date = models.DateField(_('Release date'), null=True, db_index=True)
    is_promo = models.BooleanField(_('Promo card'), default=False)
    is_original = models.BooleanField(_('Original card'), default=False)

    # Skill info

    SKILL_TYPES = OrderedDict([
        (1, {
            'translation': _(u'Score up'),
            'english': 'Score up',
            'japanese_translation': u'スコアＵＰ',
            'icon': 'scoreup',

            # Main skill
            'variables': ['duration', 'percentage'],
            'template': _(u'For the next {duration} seconds, score of all notes boosted by +{percentage}%'),
            'special_templates': {
                'perfect_only': _(u'For the next {duration} seconds, score of PERFECT notes boosted by +{percentage}%'),
                'based_on_stamina': _(u'For the next {duration} seconds, if life is {stamina} or above, score boosted by +{percentage}%, otherwise, score boosted by +{alt_percentage}%'),
            },
            'special_variables': {
                'perfect_only': ['duration', 'percentage'],
                'based_on_stamina': ['duration', 'stamina', 'percentage', 'alt_percentage'],
            },
            'japanese_template': u'{duration}スコアが{percentage}％UPする',
            'special_japanese_templates': {
                'perfect_only': u'{duration}秒間PERFECTのときのみ、スコアが{percentage}% UPする',
                'based_on_stamina': u'{duration}秒間スコアが{percentage}%UP、発動時に自分のライフが{stamina}以上の場合はスコアが{alt_percentage}%UPする',
            },

            # Side skill
            'side_variables': ['duration', 'percentage'],
            'side_template': _(u'and boosts score of all notes by {percentage}% for the next {duration} seconds'),
            'side_japanese_template': u'、{duration}秒間スコアが {percentage}%UPする',
        }),
        (2, {
            'translation': _(u'Life recovery'),
            'english': 'Life recovery',
            'japanese_translation': u'ライフ回復',
            'icon': 'healer',

            # Main skill
            'variables': ['stamina'],
            'template': _(u'Restores life by {stamina}'),
            'japanese_template': u'ライフが{stamina}回復し',

            # Side skill
            'side_variables': ['stamina'],
            'side_template': _(u'and restores life by {stamina}'),
            'side_japanese_template': u'、ライフが {stamina} 回復し',
        }),
        (3, {
            'translation': _(u'Perfect lock'),
            'english': 'Perfect lock',
            'japanese_translation': u'判定強化',
            'icon': 'perfectlock',

            # Main skill
            'variables': ['note_type'],
            'template': _(u'All {note_type} notes turn into PERFECT notes'),
            'japanese_template': u'{note_type} 以上がすべてPERFECTになり',

            # Side skill
            'side_variables': ['duration', 'note_type'],
            'side_template': _(u'and turn all {note_type} notes turn into PERFECT notes for the next {duration} seconds'),
            'side_japanese_template': u'{duration}秒間{note_type}以上がすべてPERFECTになる',
        }),
    ])

    SKILL_SPECIAL_CHOICES = (
        ('perfect_only', 'Boost score limited to perfect notes'),
        ('based_on_stamina', 'Boost score based on stamina'),
    )

    ALL_VARIABLES = { item: True for sublist in [ _info['variables'] + _info['side_variables'] + [ii for sl in [_i for _i in _info.get('special_variables', {}).values()] for ii in sl] for _info in SKILL_TYPES.values() ] for item in sublist }.keys()
    VARIABLES_PER_SKILL_TYPES = {
        'skill': { _skill_type: _info['variables'] for _skill_type, _info in SKILL_TYPES.items() },
        'side_skill': { _skill_type: _info['side_variables'] for _skill_type, _info in SKILL_TYPES.items() },
    }
    SPECIAL_CASES_VARIABLES = { _skill_type: { _i: _v for _i, _v in enumerate(_info['special_variables'].values()) } for _skill_type, _info in SKILL_TYPES.items() if 'special_variables' in _info }

    TEMPLATE_PER_SKILL_TYPES = {
        'skill': { _skill_type: unicode(_info['template']) for _skill_type, _info in SKILL_TYPES.items() },
        'side_skill': { _skill_type: unicode(_info['side_template']) for _skill_type, _info in SKILL_TYPES.items() },
    }
    SPECIAL_CASES_TEMPLATE = { _skill_type: { _i: unicode(_v) for _i, _v in enumerate(_info['special_templates'].values()) } for _skill_type, _info in SKILL_TYPES.items() if 'special_templates' in _info }

    # Main skill

    skill_name = models.CharField(_('Skill name'), max_length=100, null=True)
    japanese_skill_name = models.CharField(string_concat(_('Skill name'), ' (', t['Japanese'], ')'), max_length=100, null=True)
    SKILL_NAMES_CHOICES = ALT_LANGUAGES_EXCEPT_JP
    d_skill_names = models.TextField(_('Skill name'), null=True)

    @property
    def t_skill_name(self):
        if get_language() == 'ja':
            return self.japanese_skill_name
        return self.skill_names.get(get_language(), self.skill_name)

    SKILL_TYPE_WITHOUT_I_CHOICES = True
    SKILL_TYPE_CHOICES = [(_name, _info['translation']) for _name, _info in SKILL_TYPES.items()]
    i_skill_type = models.PositiveIntegerField(_('Skill'), choices=SKILL_TYPE_CHOICES, null=True, db_index=True)
    japanese_skill_type = property(getInfoFromChoices('skill_type', SKILL_TYPES, 'japanese_translation'))
    skill_icon = property(getInfoFromChoices('skill_type', SKILL_TYPES, 'icon'))
    @property
    def skill_template(self):
        return self.SKILL_TYPES[self.skill_type].get('special_templates', {}).get(self.skill_special, self.SKILL_TYPES[self.skill_type]['template'])
    @property
    def japanese_skill_template(self):
        return self.SKILL_TYPES[self.skill_type].get('special_japanese_templates', {}).get(self.skill_special, self.SKILL_TYPES[self.skill_type]['japanese_template'])

    @property
    def skill_variables(self):
        return {
            key: getattr(self, u'skill_{}'.format(key))
            for key in self.SPECIAL_CASES_VARIABLES.get(self.skill_type, {}).get(self.i_skill_special, self.VARIABLES_PER_SKILL_TYPES['skill'].get(self.skill_type, []))
        }

    @property
    def skill(self):
        if self.i_skill_type is None: return None
        return self.skill_template.format(**self.skill_variables)

    @property
    def japanese_skill(self):
        if self.i_skill_type is None: return None
        return self.japanese_skill_template.format(**self.skill_variables)

    # Side skill

    SIDE_SKILL_TYPE_CHOICES = SKILL_TYPE_CHOICES
    SIDE_SKILL_TYPE_WITHOUT_I_CHOICES = True
    i_side_skill_type = models.PositiveIntegerField('Side skill', choices=SIDE_SKILL_TYPE_CHOICES, null=True, db_index=True)
    japanese_side_skill_type = property(getInfoFromChoices('side_skill_type', SKILL_TYPES, 'japanese_translation'))
    side_skill_template = property(getInfoFromChoices('side_skill_type', SKILL_TYPES, 'side_template'))
    japanese_side_skill_template = property(getInfoFromChoices('side_skill_type', SKILL_TYPES, 'side_japanese_template'))
    side_skill_icon = property(getInfoFromChoices('side_skill_type', SKILL_TYPES, 'icon'))

    @property
    def side_skill_variables(self):
        return {
            key: getattr(self, u'skill_{}'.format(key))
            for key in self.SKILL_TYPES[self.side_skill_type]['side_variables']
        }

    @property
    def side_skill(self):
        if self.i_side_skill_type is None: return None
        return self.side_skill_template.format(**self.side_skill_variables)

    @property
    def japanese_side_skill(self):
        if self.i_side_skill_type is None: return None
        return self.japanese_side_skill_template.format(**self.side_skill_variables)

    # Full skill

    @property
    def full_skill(self):
        if not self.i_skill_type: return None
        return u'{} {}'.format(
            self.skill,
            self.side_skill if self.i_side_skill_type else u'',
        )

    @property
    def japanese_full_skill(self):
        if not self.i_skill_type: return None
        return u'{} {}'.format(
            self.japanese_skill,
            self.japanese_side_skill if self.i_side_skill_type else u'',
        )

    # Skill variables

    i_skill_special = models.PositiveIntegerField('Skill details - Special case', choices=i_choices(SKILL_SPECIAL_CHOICES), null=True)

    SKILL_NOTE_TYPE_CHOICES = (
        'MISS',
        'BAD',
        'GOOD',
        'GREAT',
        'PERFECT',
    )
    i_skill_note_type = models.PositiveIntegerField('{note_type}', choices=i_choices(SKILL_NOTE_TYPE_CHOICES), null=True)
    skill_stamina = models.PositiveIntegerField('{stamina}', null=True)
    skill_duration = models.PositiveIntegerField('{duration}', null=True, help_text='in seconds')
    skill_percentage = models.FloatField('{percentage}', null=True, help_text='0-100')
    skill_alt_percentage = models.FloatField('{alt_percentage}', null=True, help_text='0-100')

    # Images
    _original_image = models.ImageField(null=True, upload_to=uploadTiny('c'))
    image = models.ImageField(_('Icon'), upload_to=uploadItem('c'), null=True)
    _original_image_trained = models.ImageField(null=True, upload_to=uploadTiny('c/a'))
    image_trained = models.ImageField(string_concat(_('Icon'), ' (', _('Trained'), ')'), upload_to=uploadItem('c/a'), null=True)

    tinypng_settings = {
        'art': {
            'resize': 'scale',
            'height': 402,
        },
        'art_trained': {
            'resize': 'scale',
            'height': 402,
        },
    }

    _original_art = models.ImageField(null=True, upload_to=uploadTiny('c/art'))
    _tthumbnail_art = models.ImageField(null=True, upload_to=uploadTthumb('c/art'))
    _2x_art = models.ImageField(null=True, upload_to=upload2x('c/art'))
    art = models.ImageField(_('Art'), upload_to=uploadItem('c/art'), null=True)
    show_art_on_homepage = models.BooleanField(default=True)

    _original_art_trained = models.ImageField(null=True, upload_to=uploadTiny('c/art/a'))
    _tthumbnail_art_trained = models.ImageField(null=True, upload_to=uploadTthumb('c/art/a'))
    _2x_art_trained = models.ImageField(null=True, upload_to=upload2x('c/art/a'))
    art_trained = models.ImageField(string_concat(_('Art'), ' (', _('Trained'), ')'), upload_to=uploadItem('c/art/a'), null=True)
    show_trained_art_on_homepage = models.BooleanField(default=True)

    _tthumbnail_transparent = models.ImageField(null=True, upload_to=uploadTthumb('c/transparent'))
    _2x_transparent = models.ImageField(null=True, upload_to=upload2x('c/transparent'))
    transparent = models.ImageField(_('Transparent'), upload_to=uploadItem('c/transparent'), null=True)

    _tthumbnail_transparent_trained = models.ImageField(null=True, upload_to=uploadTthumb('c/transparent/a'))
    _2x_transparent_trained = models.ImageField(null=True, upload_to=upload2x('c/transparent/a'))
    transparent_trained = models.ImageField(string_concat(_('Transparent'), ' (', _('Trained'), ')'), upload_to=uploadItem('c/transparent/a'), null=True)

    # Statistics
    performance_min = models.PositiveIntegerField(string_concat(_('Performance'), ' (', _('Minimum'), ')'), default=0)
    performance_max = models.PositiveIntegerField(string_concat(_('Performance'), ' (', _('Maximum'), ')'), default=0)
    performance_trained_max = models.PositiveIntegerField(string_concat(_('Performance'), ' (', _('Trained'), ', ', _('Maximum'), ')'), default=0)
    technique_min = models.PositiveIntegerField(string_concat(_('Technique'), ' (', _('Minimum'), ')'), default=0)
    technique_max = models.PositiveIntegerField(string_concat(_('Technique'), ' (', _('Maximum'), ')'), default=0)
    technique_trained_max = models.PositiveIntegerField(string_concat(_('Technique'), ' (', _('Trained'), ', ', _('Maximum'), ')'), default=0)
    visual_min = models.PositiveIntegerField(string_concat(_('Visual'), ' (', _('Minimum'), ')'), default=0)
    visual_max = models.PositiveIntegerField(string_concat(_('Visual'), ' (', _('Maximum'), ')'), default=0)
    visual_trained_max = models.PositiveIntegerField(string_concat(_('Visual'), ' (', _('Trained'), ', ', _('Maximum'), ')'), default=0)

    @property
    def overall_min(self):
        return self.performance_min + self.technique_min + self.visual_min
    @property
    def overall_max(self):
        return self.performance_max + self.technique_max + self.visual_max
    @property
    def overall_trained_max(self):
        return self.performance_trained_max + self.technique_trained_max + self.visual_trained_max

    # Other members that appear in the card art
    cameo_members = models.ManyToManyField(Member, related_name='cameo_members', verbose_name=_('Cameos'))

    # Tools

    TRAINABLE_RARITIES = [3, 4]

    @property
    def trainable(self):
        return self.i_rarity in self.TRAINABLE_RARITIES

    MAX_LEVELS = {
        1: 20,
        2: 30,
        3: (40, 50),
        4: (50, 60),
    }

    @property
    def max_level(self):
        return self.MAX_LEVELS[self.i_rarity][0] if self.trainable else self.MAX_LEVELS[self.i_rarity]

    @property
    def max_level_trained(self):
        return self.MAX_LEVELS[self.i_rarity][1] if self.trainable else self.MAX_LEVELS[self.i_rarity]

    # All Stats

    @property
    def statuses(self):
        statuses = [
            ('min', _('Level {level}').format(level=1)),
            ('max', _('Level {level}').format(level=self.max_level)),
        ]
        if self.trainable:
            statuses.append(('trained_max', _('Level {level}').format(level=self.max_level_trained)))
        return statuses

    _local_stats = None

    @property
    def stats_percent(self):
        if not self._local_stats:
            self._local_stats = [
                (status, [(
                    field,
                    localized,
                    getattr(self, field + '_' + status),
                    django_settings.MAX_STATS[field + '_max'],
                    (getattr(self, field + '_' + status) / (django_settings.MAX_STATS[field + '_' + ('trained_max' if self.trainable else 'max')] or 1)) * 100,
                ) for (field, localized) in [
                    ('performance', _('Performance')),
                    ('technique', _('Technique')),
                    ('visual', _('Visual')),
                    ('overall', _('Overall')),
                ]]) for status, localized in self.statuses
            ]
        return self._local_stats

    # Cache member

    _cache_member_days = 20
    _cache_member_last_update = models.DateTimeField(null=True)
    _cache_j_member = models.TextField(null=True)

    @classmethod
    def cached_member_pre(self, d):
        d['name'] = d['names'].get('en', None)
        d['t_name'] = d['unicode'] = d['names'].get(get_language(), d['name'])

    def to_cache_member(self):
        if not self.member:
            return {
                'id': None,
                'names': {},
                'image': None,
            }
        names = self.member.names or {}
        names['en'] = self.member.name
        names['ja'] = self.member.japanese_name
        return {
            'id': self.member_id,
            'names': names,
            'image': unicode(self.member.square_image),
        }

    # Cache events

    _cached_events_collection_name = 'event'
    _cache_events_days = 20
    _cache_events_last_update = models.DateTimeField(null=True)
    _cache_j_events = models.TextField(null=True)

    @classmethod
    def cached_events_pre(self, d):
        d['name'] = d['names'].get('en', None)
        d['japanese_name'] = d['names'].get('ja', None)
        d['t_name'] = d['unicode'] = d['names'].get(get_language(), d['name'])

    def to_cache_events(self):
        events = []
        for event in Event.objects.filter(Q(main_card_id=self.id) | Q(secondary_card_id=self.id)):
            names = event.names or {}
            names['en'] = event.name
            names['ja'] = event.japanese_name
            events.append({
                'id': event.id,
                'names': names,
                'image': unicode(event.image),
            })
        return events if events else None

    # Cache gachas

    _cached_gachas_collection_name = 'gacha'
    _cache_gachas_days = 20
    _cache_gachas_last_update = models.DateTimeField(null=True)
    _cache_j_gachas = models.TextField(null=True)

    @classmethod
    def cached_gachas_pre(self, d):
        d['name'] = d['names'].get('en', None)
        d['japanese_name'] = d['names'].get('ja', None)
        d['t_name'] = d['unicode'] = d['names'].get(get_language(), d['name'])

    def to_cache_gachas(self):
        gachas = []
        for gacha in Gacha.objects.filter(cards__id=self.id):
            names = gacha.names or {}
            names['en'] = gacha.name
            names['ja'] = gacha.japanese_name
            gachas.append({
                'id': gacha.id,
                'names': names,
                'image': unicode(gacha.image),
            })
        return gachas if gachas else None

    # Cache cameos

    _cached_cameos_collection_name = 'member'
    _cache_cameos_days = 200
    _cache_cameos_last_update = models.DateTimeField(null=True)
    _cache_j_cameos = models.TextField(null=True)

    def to_cache_cameos(self):
        return [{
            'id': cameo.id,
            'name': unicode(cameo.name),
            'japanese_name': unicode(cameo.japanese_name),
            'image': unicode(cameo.square_image),
        } for cameo in self.cameo_members.all()]

    @classmethod
    def cached_cameos_pre(self, d):
        d['unicode'] = d['japanese_name'] if get_language() == 'ja' else d['name']
        return d

    # Cache totals

    reverse_related = (
        ('favorited', 'favoritecards', lambda: _('Favorite {things}').format(things=_('Cards').lower())),
        ('collectedcards', 'collectiblecards', lambda: _('Collected {things}').format(things=_('Cards').lower())),
    )

    _cache_total_favorited_days = 1
    _cache_total_favorited_last_update = models.DateTimeField(null=True)
    _cache_total_favorited = models.PositiveIntegerField(null=True)

    def to_cache_total_favorited(self):
        return self.favorited.all().count()

    _cache_total_collectedcards_days = 1
    _cache_total_collectedcards_last_update = models.DateTimeField(null=True)
    _cache_total_collectedcards = models.PositiveIntegerField(null=True)

    def to_cache_total_collectedcards(self):
        return self.collectedcards.all().count()

    ########

    @property # To allow favorite card to use the same template
    def card(self):
        return self

    def __unicode__(self):
        if self.id:
            return u'{rarity} {member_name} - {attribute}{name}'.format(
                rarity=self.t_rarity,
                member_name=self.cached_member.t_name if self.cached_member else '',
                attribute=self.t_attribute,
                name=u' - {}'.format(self.t_name) if self.t_name else '',
            )
        return u''

############################################################
# Collectible Cards

class CollectibleCard(AccountAsOwnerModel):
    collection_name = 'collectiblecard'

    account = models.ForeignKey(Account, verbose_name=_('Account'), related_name='cardscollectors')
    card = models.ForeignKey(Card, verbose_name=_('Card'), related_name='collectedcards')
    trained = models.BooleanField(_('Trained'), default=False)
    prefer_untrained = models.BooleanField(_('Prefer untrained card image'), default=False)
    max_leveled = models.NullBooleanField(_('Max Leveled'))
    first_episode = models.NullBooleanField(_('{nth} episode').format(nth=_('1st')))
    memorial_episode = models.NullBooleanField(_('Memorial episode'))
    skill_level = models.PositiveIntegerField(_('Skill level'), null=True, blank=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ])

    @property
    def image(self):
        return self.card.image_trained if self.trained and not self.prefer_untrained else self.card.image

    @property
    def image_url(self):
        return self.card.image_trained_url if self.trained and not self.prefer_untrained else self.card.image_url

    @property
    def http_image_url(self):
        return self.card.http_image_trained_url if self.trained and not self.prefer_untrained else self.card.http_image_url

    @property
    def art(self):
        return self.card.art_trained if self.trained and not self.prefer_untrained else self.card.art

    @property
    def art_url(self):
        return self.card.art_trained_url if self.trained and not self.prefer_untrained else self.card.art_url

    @property
    def http_art_url(self):
        return self.card.http_art_trained_url if self.trained and not self.prefer_untrained else self.card.http_art_url

    @property
    def art_url_original(self):
        return self.card.art_trained_original_url if self.trained and not self.prefer_untrained else self.card.art_original_url

    @property
    def color(self):
        return self.card.english_attribute

    @property
    def full_skill(self):
        if self.card.skill_duration:
            self.previous_duration = self.card.skill_duration
            self.card.skill_duration = self.card.skill_duration + (((self.skill_level or 1) - 1) * 0.5)
        full_skill = unicode(self.card.full_skill)
        if self.card.skill_duration:
            self.card.skill_duration = self.previous_duration
        return full_skill

    def __unicode__(self):
        if self.id:
            return unicode(self.card)
        return super(CollectibleCard, self).__unicode__()

class FavoriteCard(MagiModel):
    collection_name = 'favoritecard'

    owner = models.ForeignKey(User, related_name='favorite_cards')
    card = models.ForeignKey(Card, verbose_name=_('Card'), related_name='favorited')

    class Meta:
        unique_together = (('owner', 'card'), )

############################################################
# Events

def _event_gacha_top_image(item, image_name='image'):
    image = None
    # Check for current event and return banner of current if any
    for prefix in Account.VERSIONS_PREFIXES.values():
        status = getattr(item, u'{}status'.format(prefix))
        if status and status != 'ended':
            image = getattr(item, u'{}{}_url'.format(prefix, image_name))
            break
    # Otherwise, return banner that makes more sense for the language the users uses
    if not image and get_language() in LANGUAGES_TO_VERSIONS:
        image = getattr(item, u'{}{}_url'.format(Account.VERSIONS_PREFIXES[LANGUAGES_TO_VERSIONS[get_language()]], image_name))
    return image or getattr(item, u'{}_url'.format(image_name)) or staticImageURL('stars.png')

class Event(MagiModel):
    collection_name = 'event'

    owner = models.ForeignKey(User, related_name='added_events')

    _original_image = models.ImageField(null=True, upload_to=uploadTiny('e'))
    image = models.ImageField(_('Image'), upload_to=uploadItem('e'))
    top_image = property(_event_gacha_top_image)

    name = models.CharField(_('Title'), max_length=100, unique=True)
    japanese_name = models.CharField(string_concat(_('Title'), ' (', t['Japanese'], ')'), max_length=100, unique=True)
    NAMES_CHOICES = ALT_LANGUAGES_EXCEPT_JP
    d_names = models.TextField(_('Title'), null=True)

    @property
    def t_name(self):
        if get_language() == 'ja':
            return self.japanese_name
        return self.names.get(get_language(), self.name)

    TYPE_CHOICES = (
        ('normal', _('Normal')),
        ('challenge_live', _('Challenge Live')),
        ('vs_live', _('VS Live')),
        ('live_trial', _('Live Trial')),
    )
    i_type = models.PositiveIntegerField(_('Event type'), choices=i_choices(TYPE_CHOICES), default=0)

    SONG_RANKING_TYPES = [
        'challenge_live',
        'vs_live',
    ]
    TRIAL_MASTER_TYPES = [
        'live_trial',
    ]

    start_date = models.DateTimeField(string_concat(_('Japanese version'), ' - ', _('Beginning')), null=True)
    end_date = models.DateTimeField(string_concat(_('Japanese version'), ' - ',_('End')), null=True)

    TIMES_PER_VERSIONS = {
        'JP': ((6, 0), (11, 59)),
        'EN': ((1, 0), (6, 59)),
        'TW': ((7, 0), (13, 59)),
        'KR': ((6, 0), (13, 0)),
    }
    FIELDS_PER_VERSION = ['image', 'countdown', 'start_date', 'end_date', 'leaderboard', 'rerun']
    # Assets (stamps, titles) are added dynamically to the js variable because multiple can be present

    VERSIONS = Account.VERSIONS
    VERSIONS_CHOICES = Account.VERSION_CHOICES
    c_versions = models.TextField(_('Server availability'), blank=True, null=True, default='"JP"')

    _original_english_image = models.ImageField(null=True, upload_to=uploadTiny('e/e'))
    english_image = models.ImageField(string_concat(_('English version'), ' - ', _('Image')), upload_to=uploadItem('e/e'), null=True)
    english_start_date = models.DateTimeField(string_concat(_('English version'), ' - ', _('Beginning')), null=True)
    english_end_date = models.DateTimeField(string_concat(_('English version'), ' - ', _('End')), null=True)

    _original_taiwanese_image = models.ImageField(null=True, upload_to=uploadTiny('e/t'))
    taiwanese_image = models.ImageField(string_concat(_('Taiwanese version'), ' - ', _('Image')), upload_to=uploadItem('e/t'),  null=True)
    taiwanese_start_date = models.DateTimeField(string_concat(_('Taiwanese version'), ' - ', _('Beginning')), null=True)
    taiwanese_end_date = models.DateTimeField(string_concat(_('Taiwanese version'), ' - ', _('End')), null=True)

    _original_korean_image = models.ImageField(null=True, upload_to=uploadTiny('e/t'))
    korean_image = models.ImageField(string_concat(_('Korean version'), ' - ', _('Image')), upload_to=uploadItem('e/t'),  null=True)
    korean_start_date = models.DateTimeField(string_concat(_('Korean version'), ' - ', _('Beginning')), null=True)
    korean_end_date = models.DateTimeField(string_concat(_('Korean version'), ' - ', _('End')), null=True)

    MAIN_CARD_ALLOWED_RARITIES = (3,)
    SECONDARY_CARD_ALLOWED_RARITIES = (3, 2)

    main_card = models.ForeignKey(Card, related_name='main_card_event', null=True, limit_choices_to={
        'i_rarity__in': MAIN_CARD_ALLOWED_RARITIES,
    }, on_delete=models.SET_NULL)
    secondary_card = models.ForeignKey(Card, related_name='secondary_card_event', null=True, limit_choices_to={
        'i_rarity__in': SECONDARY_CARD_ALLOWED_RARITIES,
    }, on_delete=models.SET_NULL)

    BOOST_ATTRIBUTE_CHOICES = Card.ATTRIBUTE_CHOICES
    BOOST_ATTRIBUTE_WITHOUT_I_CHOICES = True
    i_boost_attribute = models.PositiveIntegerField(_('Boost attribute'), choices=BOOST_ATTRIBUTE_CHOICES, null=True)
    english_boost_attribute = property(getInfoFromChoices('boost_attribute', Card.ATTRIBUTES, 'english'))

    boost_members = models.ManyToManyField(Member, related_name='boost_in_events', verbose_name=_('Boost members'))

    @property
    def cached_gacha(self):
        # No need for a cache because the gacha is select_related in item view
        self.gacha.unicode = unicode(self.gacha)
        return self.gacha

    def get_status(self, version='JP'):
        start_date = getattr(self, u'{}start_date'.format(Account.VERSIONS_PREFIXES[version]))
        end_date = getattr(self, u'{}end_date'.format(Account.VERSIONS_PREFIXES[version]))
        return getEventStatus(start_date, end_date)

    status = property(lambda _s: _s.get_status())
    english_status = property(lambda _s: _s.get_status(version='EN'))
    taiwanese_status = property(lambda _s: _s.get_status(version='TW'))
    korean_status = property(lambda _s: _s.get_status(version='KR'))

    # Cache totals

    reverse_related = (
        ('participations', 'eventparticipations', _('Participated events')),
    )

    _cache_total_participations_days = 1
    _cache_total_participations_last_update = models.DateTimeField(null=True)
    _cache_total_participations = models.PositiveIntegerField(null=True)

    def to_cache_total_participations(self):
        return self.participations.all().count()

    ########

    def __unicode__(self):
        return self.t_name

############################################################
# Collectible Event

class EventParticipation(AccountAsOwnerModel):
    collection_name = 'eventparticipation'

    account = models.ForeignKey(Account, verbose_name=_('Account'), related_name='events')
    event = models.ForeignKey(Event, verbose_name=_('Event'), related_name='participations')

    score = models.PositiveIntegerField(_('Score'), null=True)
    ranking = models.PositiveIntegerField(_('Ranking'), null=True)

    song_score = models.PositiveIntegerField(_('Song score'), null=True)
    song_ranking = models.PositiveIntegerField(_('Song ranking'), null=True)

    is_trial_master_completed = models.NullBooleanField(_('Trial master completed'))
    is_trial_master_ex_completed = models.NullBooleanField(_('Trial master EX completed'))

    _thumbnail_screenshot = models.ImageField(null=True, upload_to=uploadThumb('event_screenshot'))
    screenshot = models.ImageField(_('Screenshot'), upload_to=uploadItem('event_screenshot'), null=True)

    @property
    def ranking_image_url(self):
        return get_image_url_from_path(u'static/img/badges/medal{}.png'.format(4 - self.ranking))

    @property
    def leaderboard_details(self):
        return [(k, v) for k, v in [
            ('score', {
                'icon': 'scoreup',
                'verbose_name': _('Score'),
                'value': self.score,
            }),
            ('song_score', {
                'icon': 'song',
                'verbose_name': _('Song score'),
                'value': self.song_score,
            }),
            ('song_ranking', {
                'icon': 'contest',
                'verbose_name': _('Song ranking'),
                'value': self.song_ranking,
            }),
            ('is_trial_master_completed', {
                'icon': 'achievement',
                'verbose_name': _('Trial master completed'),
                'value': self.is_trial_master_completed,
            }),
            ('is_trial_master_ex_completed', {
                'icon': 'achievement',
                'verbose_name': _('Trial master EX completed'),
                'value': self.is_trial_master_ex_completed,
            }),
        ] if v['value'] and not (
            (k in ['song_score', 'song_ranking'] and self.event.type not in Event.SONG_RANKING_TYPES)
            and (k in ['is_trial_master_completed', 'is_trial_master_ex_completed']
                 and self.event.type not in Event.TRIAL_MASTER_TYPES)
        )]

    def to_cache_account(self):
        d = super(EventParticipation, self).to_cache_account()
        d['i_version'] = self.account.i_version
        return d

    @property
    def image(self):
        return getattr(self.event, u'{}image'.format(Account.VERSIONS_PREFIXES[self.cached_account.version])) or self.event.image

    @property
    def image_url(self):
        return getattr(self.event, u'{}image_url'.format(Account.VERSIONS_PREFIXES[self.cached_account.version])) or self.event.image_url

    @property
    def http_image_url(self):
        return getattr(self.event, u'http_{}image_url'.format(Account.VERSIONS_PREFIXES[self.cached_account.version])) or self.event.http_image_url

    def __unicode__(self):
        if self.id:
            return unicode(self.event)
        return super(EventParticipation, self).__unicode__()

############################################################
# Song

class Song(MagiModel):
    collection_name = 'song'

    DIFFICULTY_VALIDATORS = [
        MinValueValidator(1),
        MaxValueValidator(50),
    ]

    DIFFICULTIES = [
        ('easy', _('Easy')),
        ('normal', _('Normal')),
        ('hard', _('Hard')),
        ('expert', _('Expert')),
        ('special', _('Special')),
    ]

    SONGWRITERS_DETAILS = [
        ('composer', _('Composer')),
        ('lyricist', _('Lyricist')),
        ('arranger', _('Arranger')),
    ]

    owner = models.ForeignKey(User, related_name='added_songs')
    _original_image = models.ImageField(null=True, upload_to=uploadTiny('s'))
    image = models.ImageField('Album cover', upload_to=uploadItem('s'))

    BAND_CHOICES = list(Member.BAND_CHOICES) + ['Glitter*Green', 'Special Band']
    i_band = models.PositiveIntegerField(_('Band'), choices=i_choices(BAND_CHOICES))

    special_band = models.CharField(_('Band'), max_length=100, null=True)
    SPECIAL_BANDS_CHOICES = LANGUAGES_DIFFERENT_CHARSET
    d_special_bands = models.TextField(_('Band'), null=True)

    japanese_name = models.CharField(_('Title'), max_length=100, unique=True)
    romaji_name = models.CharField(string_concat(_('Title'), ' (', _('Romaji'), ')'), max_length=100, null=True)
    name = models.CharField(string_concat(_('Title'), ' (', _('Translation'), ')'), max_length=100, null=True)
    NAMES_CHOICES = ALT_LANGUAGES_EXCEPT_JP
    d_names = models.TextField(_('Title'), null=True)

    @property
    def t_name(self):
        if get_language() == 'ja':
            return self.japanese_name
        return self.names.get(get_language(), self.name)

    VERSIONS = Account.VERSIONS
    VERSIONS_CHOICES = Account.VERSION_CHOICES
    c_versions = models.TextField(_('Server availability'), blank=True, null=True, default='"JP"')

    itunes_id = models.PositiveIntegerField(_('Preview'), help_text='iTunes ID', null=True)
    length = models.PositiveIntegerField(_('Length'), null=True)

    @property
    def length_in_minutes(self):
        return time.strftime('%M:%S', time.gmtime(self.length))

    is_cover = models.BooleanField(_('Cover song'), default=False)
    bpm = models.PositiveIntegerField(_('Beats per minute'), null=True)
    release_date = models.DateField(_('Release date'), null=True)

    composer = models.CharField(_('Composer'), max_length=100, null=True)
    lyricist = models.CharField(_('Lyricist'), max_length=100, null=True)
    arranger = models.CharField(_('Arranger'), max_length=100, null=True)

    easy_notes = models.PositiveIntegerField(string_concat(_('Easy'), ' - ', _('Notes')), null=True)
    easy_difficulty = models.PositiveIntegerField(string_concat(_('Easy'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    normal_notes = models.PositiveIntegerField(string_concat(_('Normal'), ' - ', _('Notes')), null=True)
    normal_difficulty = models.PositiveIntegerField(string_concat(_('Normal'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    hard_notes = models.PositiveIntegerField(string_concat(_('Hard'), ' - ', _('Notes')), null=True)
    hard_difficulty = models.PositiveIntegerField(string_concat(_('Hard'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    expert_notes = models.PositiveIntegerField(string_concat(_('Expert'), ' - ', _('Notes')), null=True)
    expert_difficulty = models.PositiveIntegerField(string_concat(_('Expert'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    special_notes = models.PositiveIntegerField(string_concat(_('Special'), ' - ', _('Notes')), null=True)
    special_difficulty = models.PositiveIntegerField(string_concat(_('Special'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)

    UNLOCK = OrderedDict([
        ('gift', {
            'translation': _('Gift'),
            'template': string_concat(_('Gift'), ' ({occasion})'),
            'variables': ['occasion'],
        }),
        ('purchase', {
            'translation': _('Purchase at CiRCLE'),
            'template': _('Purchase at CiRCLE'),
            'variables': [],
        }),
        ('complete_story', {
            'translation': _('Complete story'),
            'template': _('Complete {story_type} story, chapter {chapter}'),
            'variables': ['story_type', 'chapter'],
        }),
        ('complete_tutorial', {
            'translation': _('Complete Tutorial'),
            'template': _('Complete Tutorial'),
            'variables': [],
        }),
        ('initial', {
            'translation': _('Initially available'),
            'template': _('Initially available'),
            'variables': [],
        }),
        ('event', {
            'translation': _('Event gift'),
            'template': _('Event gift'),
            'variables': [],
        }),
        ('other', {
            'translation': _('Other'),
            'template': '{how_to_unlock}',
            'variables': ['how_to_unlock'],
        }),
    ])

    UNLOCK_CHOICES = [(_name, _info['translation']) for _name, _info in UNLOCK.items()]
    i_unlock = models.PositiveIntegerField(_('How to unlock?'), choices=i_choices(UNLOCK_CHOICES))

    c_unlock_variables = models.CharField(max_length=100, null=True)
    unlock_variables_keys = property(getInfoFromChoices('unlock', UNLOCK, 'variables'))
    unlock_template = property(getInfoFromChoices('unlock', UNLOCK, 'template'))
    @property
    def unlock_sentence(self):
        return unicode(self.unlock_template).format(**dict(zip(self.unlock_variables_keys, self.unlock_variables)))

    event = models.ForeignKey(Event, verbose_name=_('Event'), related_name='gift_songs', null=True, on_delete=models.SET_NULL)

    @property
    def cached_event(self):
        # No need for a cache because the event is select_related in item view
        self.event.unicode = unicode(self.event)
        return self.event

    @property # Needed to use with types in magicollections
    def type(self):
        return self.unlock

    # Cache totals

    reverse_related = (
        ('played', 'playedsongs', _('Played songs')),
    )

    _cache_total_played_days = 1
    _cache_total_played_last_update = models.DateTimeField(null=True)
    _cache_total_played = models.PositiveIntegerField(null=True)

    def to_cache_total_played(self):
        return self.playedby.all().count()

    ########

    def __unicode__(self):
        if get_language() == 'ja':
            return self.japanese_name
        if not self.romaji_name:
            return self.t_name or self.japanese_name
        if get_language() == 'en' and self.name:
            if self.name != self.romaji_name:
                return u'{} ({})'.format(
                    self.romaji_name,
                    self.name,
                )
        elif self.names.get(get_language(), None):
            if self.t_name != self.romaji_name:
                return u'{} ({})'.format(
                    self.romaji_name,
                    self.t_name,
                )
        return self.romaji_name

############################################################
# Collectible Song

class PlayedSong(AccountAsOwnerModel):
    collection_name = 'playedsong'

    account = models.ForeignKey(Account, verbose_name=_('Account'), related_name='playedsong')
    song = models.ForeignKey(Song, verbose_name=_('Song'), related_name='playedby')

    DIFFICULTY_CHOICES = (
        ('easy', _('Easy')),
        ('normal', _('Normal')),
        ('hard', _('Hard')),
        ('expert', _('Expert')),
        ('special', _('Special')),
    )

    i_difficulty = models.PositiveIntegerField(_('Difficulty'), choices=i_choices(DIFFICULTY_CHOICES), default=0)
    difficulty_image_url = property(lambda _ps: staticImageURL(_ps.difficulty, folder=u'songs', extension='png'))

    score = models.PositiveIntegerField(_('Score'), null=True)
    full_combo = models.NullBooleanField(_('Full combo'))
    all_perfect = models.NullBooleanField(_('All perfect'))

    _thumbnail_screenshot = models.ImageField(null=True, upload_to=uploadThumb('song_screenshot'))
    screenshot = models.ImageField(_('Screenshot'), upload_to=uploadItem('song_screenshot'), null=True)

    @property
    def image(self):
        return self.song.image

    @property
    def image_url(self):
        return self.song.image_url

    @property
    def http_image_url(self):
        return self.song.http_image_url

    @property
    def leaderboard_details(self):
        return [(k, v) for k, v in [
            ('score', {
                'icon': 'scoreup',
                'verbose_name': _('Score'),
                'value': self.score,
            }),
            ('full_combo', {
                'icon': 'combo',
                'verbose_name': _('Full combo'),
                'value': self.full_combo,
            }),
            ('all_perfect', {
                'icon': 'combo',
                'verbose_name': _('All perfect'),
                'value': self.all_perfect,
            }),
        ] if v['value']]

    def __unicode__(self):
        if self.id:
            return unicode(self.song)
        return super(PlayedSong, self).__unicode__()

############################################################
# Gacha

class Gacha(MagiModel):
    collection_name = 'gacha'

    owner = models.ForeignKey(User, related_name='added_gacha')

    _original_image = models.ImageField(null=True, upload_to=uploadTiny('g'))
    image = models.ImageField(_('Image'), upload_to=uploadItem('g'))
    top_image = property(_event_gacha_top_image)

    name = models.CharField(_('Title'), max_length=100, unique=True)
    japanese_name = models.CharField(string_concat(_('Title'), ' (', t['Japanese'], ')'), max_length=100, unique=True)
    NAMES_CHOICES = ALT_LANGUAGES_EXCEPT_JP
    d_names = models.TextField(_('Title'), null=True)

    @property
    def t_name(self):
        if get_language() == 'ja':
            return self.japanese_name
        return self.names.get(get_language(), self.name)

    limited = models.BooleanField(_('Limited'), default=False)
    dreamfes = models.BooleanField(default=False)

    start_date = models.DateTimeField(_('Beginning'), null=True)
    end_date = models.DateTimeField(_('End'), null=True)

    _original_english_image = models.ImageField(null=True, upload_to=uploadTiny('e/e'))
    english_image = models.ImageField(string_concat(_('English version'), ' - ', _('Image')), upload_to=uploadItem('e/e'), null=True)
    english_start_date = models.DateTimeField(string_concat(_('English version'), ' - ', _('Beginning')), null=True)
    english_end_date = models.DateTimeField(string_concat(_('English version'), ' - ', _('End')), null=True)

    _original_taiwanese_image = models.ImageField(null=True, upload_to=uploadTiny('e/t'))
    taiwanese_image = models.ImageField(string_concat(_('Taiwanese version'), ' - ', _('Image')), upload_to=uploadItem('e/t'), null=True)
    taiwanese_start_date = models.DateTimeField(string_concat(_('Taiwanese version'), ' - ', _('Beginning')), null=True)
    taiwanese_end_date = models.DateTimeField(string_concat(_('Taiwanese version'), ' - ', _('End')), null=True)

    _original_korean_image = models.ImageField(null=True, upload_to=uploadTiny('e/t'))
    korean_image = models.ImageField(string_concat(_('Korean version'), ' - ', _('Image')), upload_to=uploadItem('e/t'), null=True)
    korean_start_date = models.DateTimeField(string_concat(_('Korean version'), ' - ', _('Beginning')), null=True)
    korean_end_date = models.DateTimeField(string_concat(_('Korean version'), ' - ', _('End')), null=True)

    ATTRIBUTE_CHOICES = Card.ATTRIBUTE_CHOICES
    ATTRIBUTE_WITHOUT_I_CHOICES = True
    i_attribute = models.PositiveIntegerField(_('Attribute'), choices=ATTRIBUTE_CHOICES, null=True)
    english_attribute = property(getInfoFromChoices('attribute', Card.ATTRIBUTES, 'english'))

    event = models.ForeignKey(Event, verbose_name=_('Event'), related_name='gachas', null=True, on_delete=models.SET_NULL)
    cards = models.ManyToManyField(Card, verbose_name=('Cards'), related_name='gachas')

    TIMES_PER_VERSIONS = {
        'JP': ((6, 0), (5, 59)),
        'EN': ((1, 0), (0, 59)),
        'TW': ((7, 0), (6, 59)),
        'KR': ((6, 0), (6, 0)),
    }
    FIELDS_PER_VERSION = ['image', 'countdown', 'start_date', 'end_date', 'rerun']

    VERSIONS = Account.VERSIONS
    VERSIONS_CHOICES = Account.VERSION_CHOICES
    c_versions = models.TextField(_('Server availability'), blank=True, null=True, default='"JP"')

    @property
    def cached_event(self):
        # No need for a cache because the event is select_related in item view
        self.event.unicode = unicode(self.event)
        return self.event

    def get_status(self, version='JP'):
        start_date = getattr(self, u'{}start_date'.format(Account.VERSIONS_PREFIXES[version]))
        end_date = getattr(self, u'{}end_date'.format(Account.VERSIONS_PREFIXES[version]))
        return getEventStatus(start_date, end_date)

    status = property(lambda _s: _s.get_status())
    english_status = property(lambda _s: _s.get_status(version='EN'))
    taiwanese_status = property(lambda _s: _s.get_status(version='TW'))
    korean_status = property(lambda _s: _s.get_status(version='KR'))

    def __unicode__(self):
        return self.t_name

############################################################
# Rerun gacha event

class Rerun(MagiModel):
    collection_name = 'rerun'

    event = models.ForeignKey(Event, verbose_name=_('Event'), related_name='reruns', null=True)
    gacha = models.ForeignKey(Gacha, verbose_name=_('Gacha'), related_name='reruns', null=True)

    ITEMS = ['event', 'gacha']
    ITEMS_MODELS = { 'event': Event, 'gacha': Gacha }

    fk_as_owner = 'event__owner'

    @property
    def owner(self):
        return getattr(self.event, 'owner', None) or getattr(self.gacha, 'owner', None)

    @property
    def owner_id(self):
        return getattr(self.event, 'owner_id', None) or getattr(self.gacha, 'owner_id', None)

    VERSIONS = Account.VERSIONS
    VERSION_CHOICES = Account.VERSION_CHOICES
    i_version = models.PositiveIntegerField(_('Version'), choices=i_choices(VERSION_CHOICES))
    version_timezone = property(getInfoFromChoices('version', VERSIONS, 'timezone'))
    version_prefix = property(getInfoFromChoices('version', VERSIONS, 'prefix'))

    start_date = models.DateTimeField(_('Beginning'))
    end_date = models.DateTimeField(_('End'))

    @property
    def status(self):
        return getEventStatus(self.start_date, self.end_date)

    def __unicode__(self):
        return u'Rerun {} "{}" ({}): {} - {}'.format(
            'Gacha' if self.gacha_id else 'Event',
            self.gacha or self.event,
            self.version,
            self.start_date,
            self.end_date,
        )

############################################################
# Item

class Item(MagiModel):
    collection_name = 'item'

    owner = models.ForeignKey(User, related_name='added_items')

    _original_image = models.ImageField(null=True, upload_to=uploadTiny('items'))
    image = models.ImageField(_('Image'), upload_to=uploadItem('items'))

    name = models.CharField(_('Title'), max_length=100, null=True, help_text='plural')
    NAMES_CHOICES = ALL_ALT_LANGUAGES
    d_names = models.TextField(_('Title'), null=True)

    m_description = models.TextField(_('Description'), null=True)
    M_DESCRIPTIONS_CHOICES = ALL_ALT_LANGUAGES
    d_m_descriptions = models.TextField(_('Description'), null=True)

    def __unicode__(self):
        return self.t_name

############################################################
# Collected item

class CollectibleItem(AccountAsOwnerModel):
    collection_name = 'collectibleitem'

    account = models.ForeignKey(Account, verbose_name=_('Account'), related_name='items')
    item = models.ForeignKey(Item, verbose_name=_('Item'), related_name='collectedby')

    quantity = models.PositiveIntegerField(_('Quantity'), default=1)

    image = property(lambda _s: _s.item.image)
    image_url = property(lambda _s: _s.item.image_url)
    http_image_url = property(lambda _s: _s.item.http_image_url)

    @property
    def subtitle(self):
        return u'x{}'.format(self.quantity)

    def __unicode__(self):
        if self.id:
            return unicode(self.item)
        return super(CollectibleItem, self).__unicode__()

############################################################
# Area item

class Area(MagiModel):
    collection_name = 'area'

    owner = models.ForeignKey(User, related_name='added_areas')

    _original_image = models.ImageField(null=True, upload_to=uploadTiny('areas'))
    image = models.ImageField(_('Image'), upload_to=uploadItem('areas'))

    name = models.CharField(_('Title'), max_length=100)
    NAMES_CHOICES = ALL_ALT_LANGUAGES
    d_names = models.TextField(_('Title'), null=True)

    def __unicode__(self):
        return self.t_name

class AreaItem(MagiModel):
    collection_name = 'areaitem'

    owner = models.ForeignKey(User, related_name='added_area_items')

    TYPES = OrderedDict([
        ('instrument_per_member', {
            'translation': 'Instrument per member',
            'variables': ['member', 'instrument'],
            'name_template': u'{member_name} {t_instrument}',
        }),
        ('instrument_per_band', {
            'translation': 'Instrument per band',
            'variables': ['name', 'i_band', 'instrument'],
            'name_template': u'{t_name} {t_instrument}',
        }),
        ('poster', {
            'translation': _('Poster'),
            'variables': ['i_band'],
            'name_template': u'{t_band} {t_type}',
        }),
        ('flyer', {
            'translation': _('Flyer'),
            'variables': ['i_band'],
            'name_template': u'{t_band} {t_type}',
        }),
        ('food', {
            'translation': _('Food'),
            'variables': ['name', 'i_attribute'],
        }),
        ('decoration', {
            'translation': _('Decoration'),
            'variables': ['name', 'i_attribute'],
        }),
        ('other', {
            'translation': _('Other'),
            'variables': ['name', 'i_band', 'i_stat', 'i_attribute', 'depends_on_life', 'flat'],
        }),
    ])
    TYPE_CHOICES = [(_name, _info['translation']) for _name, _info in TYPES.items()]
    i_type = models.PositiveIntegerField('Type', choices=i_choices(TYPE_CHOICES))
    type_name_template = property(getInfoFromChoices('type', TYPES, 'name_template'))

    VARIABLES = ['name', 'i_band', 'i_attribute', 'instrument', 'member', 'i_stat', 'depends_on_life', 'flat']

    _original_image = models.ImageField(null=True, upload_to=uploadTiny('areas/items'))
    image = models.ImageField(_('Image'), upload_to=uploadItem('areas/items'))
    area = models.ForeignKey(Area, verbose_name=_('Area'), null=True)
    value = models.FloatField(null=True)
    flat = models.BooleanField('Flat value', default=False, help_text='Default: Percentage')

    name = models.CharField(_('Title'), max_length=100, null=True)
    NAMES_CHOICES = ALL_ALT_LANGUAGES
    d_names = models.TextField(_('Title'), null=True)

    BAND_CHOICES = list(Member.BAND_CHOICES)
    i_band = models.PositiveIntegerField(_('Band'), choices=i_choices(BAND_CHOICES), null=True)

    ATTRIBUTE_CHOICES = Card.ATTRIBUTE_CHOICES
    ATTRIBUTE_WITHOUT_I_CHOICES = True
    i_attribute = models.PositiveIntegerField(_('Attribute'), choices=ATTRIBUTE_CHOICES, null=True)

    instrument = models.CharField(_('Instrument'), max_length=100, null=True)
    INSTRUMENTS_CHOICES = ALL_ALT_LANGUAGES
    d_instruments = models.TextField(_('Instrument'), null=True)

    member = models.ForeignKey(Member, verbose_name=_('Member'), related_name='area_items', null=True, on_delete=models.SET_NULL)

    @property
    def member_name(self):
        return FAVORITE_CHARACTERS_NAMES.get(self.member_id, None)

    STAT_CHOICES = (
        ('performance', _('Performance')),
        ('technique', _('Technique')),
        ('visual', _('Visual')),
    )
    i_stat = models.PositiveIntegerField('Statistics', choices=i_choices(STAT_CHOICES), null=True)

    depends_on_life = models.PositiveIntegerField(null=True)
    life = property(lambda _s: _s.depends_on_life)

    ###

    @property
    def formatted_name(self):
        template = self.type_name_template
        if not template:
            return unicode(self.t_name or self.t_type or u'{}: #{}'.format(_('Area items'), self.id))
        return template.format(**{
            variable: unicode(getattr(self, variable, ''))
            for variable in (templateVariables(template) or [])
        })

    @property
    def affected_members(self):
        if self.i_band is not None:
            return self.t_band
        elif self.i_attribute is not None:
            return self.t_attribute
        return _('All')

    @property
    def effect_value(self):
        if self.flat:
            return unicode(int(self.value))
        return '{percentage}%'.format(percentage=self.value)

    @property
    def affected_stat(self):
        if self.i_stat is not None:
            return unicode(self.t_stat).lower()
        return u'/'.join([unicode(stat).lower() for n, stat in self.STAT_CHOICES])

    @property
    def formatted_description(self):
        template = (
            _('{affected_members} members get +{effect_value} {affected_stat} points if life is above {life}')
            if self.depends_on_life
            else _('{affected_members} members get +{effect_value} {affected_stat} points')
        )
        return template.format(**{
            variable: unicode(getattr(self, variable, ''))
            for variable in (templateVariables(template) or [])
        })

    @property
    def max_level(self):
        return 6 if self.type == 'instrument_per_band' else 5

    def __unicode__(self):
        return self.formatted_name

############################################################
# Collected item

class CollectibleAreaItem(AccountAsOwnerModel):
    collection_name = 'collectibleareaitem'

    account = models.ForeignKey(Account, verbose_name=_('Account'), related_name='areaitems')
    areaitem = models.ForeignKey(AreaItem, verbose_name=_('Area item'), related_name='collectedby')

    level = models.PositiveIntegerField(_('Level'), default=1)

    image = property(lambda _s: _s.areaitem.image)
    image_url = property(lambda _s: _s.areaitem.image_url)
    http_image_url = property(lambda _s: _s.areaitem.http_image_url)

    formatted_name = property(lambda _s: _s.areaitem.formatted_name)

    @property
    def formatted_description(self):
        previous_value = self.areaitem.value
        self.areaitem.value += (0.5 * (self.level - 1))
        formatted_description = unicode(self.areaitem.formatted_description)
        self.areaitem.value = previous_value
        return formatted_description

    @property
    def subtitle(self):
        return _('Level {level}').format(level=self.level)

    def __unicode__(self):
        if self.id:
            return unicode(self.areaitem)
        return super(CollectibleAreaItem, self).__unicode__()

############################################################
# Assets

class Asset(MagiModel):
    collection_name = 'asset'

    owner = models.ForeignKey(User, related_name='added_assets')

    _tthumbnail_image = models.ImageField(null=True, upload_to=uploadTthumb('asset'))
    image = models.ImageField(_('Image'), upload_to=uploadItem('asset'), null=True)

    _tthumbnail_english_image = models.ImageField(null=True, upload_to=uploadTthumb('asset/e'))
    english_image = models.ImageField(string_concat(_('English version'), ' - ', _('Image')), upload_to=uploadItem('asset/e'), null=True)

    _tthumbnail_taiwanese_image = models.ImageField(null=True, upload_to=uploadTthumb('asset/t'))
    taiwanese_image = models.ImageField(string_concat(_('Taiwanese version'), ' - ', _('Image')), upload_to=uploadItem('asset/t'),  null=True)

    _tthumbnail_korean_image = models.ImageField(null=True, upload_to=uploadTthumb('asset/k'))
    korean_image = models.ImageField(string_concat(_('Korean version'), ' - ', _('Image')), upload_to=uploadItem('asset/k'),  null=True)

    def _get_top_image(self, thumbnail):
        show_image_version = 'EN'

        # Get preferred version of image from user's language
        if get_language() in LANGUAGES_TO_VERSIONS:
            show_image_version = LANGUAGES_TO_VERSIONS[get_language()]

        # Get preferred version of image from filtered choice
        if self.request:
            try:
                show_image_version = Account.get_reverse_i(
                    'version', int(self.request.GET.get('i_version', None)),
                ) or show_image_version
            except (KeyError, ValueError, TypeError):
                pass

        # Get thumbnail of image from preferred version
        image = getattr(self, u'{prefix}image{thumbnail}_url'.format(
            prefix=Account.VERSIONS[show_image_version]['prefix'],
            thumbnail='_thumbnail' if thumbnail else '',
        ), None)

        # Fallback to first image that exists
        if not image:
            for version in Account.VERSIONS.values():
                version_image = getattr(self, u'{prefix}image{thumbnail}_url'.format(
                    prefix=version['prefix'],
                    thumbnail='_thumbnail' if thumbnail else '',
                ), None)
                if version_image:
                    image = version_image
                    break

        return image or staticImageURL('stars.png')

    top_image = property(lambda _s: _s._get_top_image(thumbnail=False))
    top_image_list = property(lambda _s: _s._get_top_image(thumbnail=True))

    VARIABLES = ['name', 'i_band', 'members', 'c_tags', 'event', 'value', 'source', 'source_link', 'song']

    TYPES = OrderedDict([
        ('comic', {
            'translation': _('Comics'),
            'variables': ['name', 'i_band', 'members', 'value'],
            'to_unicode': lambda _a: _a.t_name or _('Comics'),
        }),
        ('background', {
            'translation': _('Backgrounds'),
            'variables': ['name', 'i_band', 'c_tags'],
            'to_unicode': lambda _a: u'{}{}'.format(
                _a.name or _('Backgrounds'),
                u' ({})'.format(_a.band) if _a.band else '',
            ),
        }),
        ('stamp', {
            'translation': _('Stamps'),
            'variables': ['name', 'members', 'event'],
            'image': 'stamp.png',
            'to_unicode': lambda _a: u'{event} {name}'.format(
                event=_a.event if _a.event else '',
                name=((_a.t_name if not _a.event else u'“{name}”'.format(name=_a.t_name))
                      if _a.name else (_('Stamps') if not _a.event else _('Rare stamp'))),
            ),
        }),
        ('title', {
            'translation': _('Titles'),
            'variables': ['name', 'event', 'song', 'value'],
            'to_unicode': lambda _a: u'{event}{song}{name}'.format(
                event=_a.event if _a.event else '',
                song=u'{dash}{song}'.format(
                    dash=u' - ' if _a.event else '',
                    song=_a.song) if _a.song else '',
                name=u'{dash}{name}{value}'.format(
                    dash=u' - ' if _a.event or _a.song else '',
                    name=_a.t_name if _a.name else '',
                    value=u' {value}'.format(value=_a.value) if _a.value and _a.name else (
                        _a.value if _a.value else ''),
                ) if _a.name or _a.value else '',
            ),
        }),
        ('interface', {
            'translation': _('Interface'),
            'variables': ['name'],
            'to_unicode': lambda _a: _a.t_name or _('Interface'),
        }),
        ('official', {
            'translation': _('Official art'),
            'variables': ['name', 'i_band', 'members', 'song', 'c_tags', 'source', 'source_link'],
            'to_unicode': lambda _a: (
                _a.t_name
                or _a.song
                or _a.band
                or u', '.join([member.t_name for member in getattr(_a, 'all_members', [])])
                or _('Official art')
            ),
        }),
    ])
    TYPE_CHOICES = [(_name, _info['translation']) for _name, _info in TYPES.items()]
    i_type = models.PositiveIntegerField('Type', choices=i_choices(TYPE_CHOICES), null=True)
    type_variables = property(getInfoFromChoices('type', TYPES, 'variables'))
    type_per_line = property(getInfoFromChoices('type', TYPES, 'per_line'))
    to_unicode = property(getInfoFromChoices('type', TYPES, 'to_unicode'))
    type_image = property(getInfoFromChoices('type', TYPES, 'image'))
    type_icon = 'pictures'

    name = models.CharField(_('Title'), max_length=100, null=True)
    NAMES_CHOICES = ALL_ALT_LANGUAGES
    d_names = models.TextField(_('Title'), null=True)

    BAND_CHOICES = Member.BAND_CHOICES
    i_band = models.PositiveIntegerField(_('Band'), choices=i_choices(BAND_CHOICES), null=True)

    members = models.ManyToManyField(Member, related_name='assets', verbose_name=_('Members'), null=True)

    TAGS_CHOICES = (
        ('outdoor', _('Outdoor')),
        ('indoor', _('Indoor')),
        ('school', _('School')),
        ('stage', _('Stage')),
        ('home', _('Home')),
        ('date', _('Dating spot')),
        ('transparent', _('Transparent')),
        ('login', _('Login')),
        ('twitter', 'Twitter'),
        ('bluray', 'Blu-ray'),
        ('cd', _('CD cover')),
        ('collab', _('Collab')),
        ('dengeki', _('Dengeki G\'s magazine')),
        ('seasonal', _('Seasonal')),
        ('birthday', _('Birthday')),
        ('live', _('Live')),
    )
    c_tags = models.TextField(_('Tags'), null=True)

    event = models.ForeignKey(Event, verbose_name=_('Event'), related_name='assets', null=True, on_delete=models.SET_NULL)
    song = models.ForeignKey(Song, verbose_name=_('Song'), related_name='assets', null=True, on_delete=models.SET_NULL)

    source = models.CharField(_('Source'), max_length=100, null=True)
    source_link = models.CharField(max_length=100, null=True)

    value = models.PositiveIntegerField(null=True)

    @property
    def tinypng_settings(self):
        # Don't generate thumbnails for titles + stamps, just use TinyPNG to compress (hacky)
        if self.type in ['title', 'stamp']:
            return {
                '_tthumbnail_{}image'.format(version_prefix): {
                    'resize': None,
                } for version_prefix in Account.VERSIONS_PREFIXES.values()
            }
        return {}

    @property
    def item_url(self):
        item_url = MagiModel.item_url.fget(self)
        if self.request and self.request.GET.get('i_version', None):
            return u'{}?i_version={}'.format(
                item_url,
                self.request.GET['i_version'],
            )
        return item_url

    @property
    def ajax_item_url(self):
        item_url = MagiModel.ajax_item_url.fget(self)
        if self.request and self.request.GET.get('i_version', None):
            return u'{}?i_version={}'.format(
                item_url,
                self.request.GET['i_version'],
            )
        return item_url

    def __unicode__(self):
        return unicode(self.to_unicode(self))

############################################################
# Costume

class Chibi(BaseMagiModel):
    _original_image = models.ImageField(upload_to=uploadTiny('cos/chibi'), null=True)
    image = models.ImageField(upload_to=uploadItem('cos/chibi'))
    costume = models.ForeignKey('Costume', verbose_name=_('Costume'), related_name='owned_chibis', on_delete=models.CASCADE)

    def __unicode__(self):
        return unicode(self.image)

class Costume(MagiModel):
    collection_name = 'costume'
    owner = models.ForeignKey(User, related_name='added_costume')

    COSTUME_TYPE_CHOICES = OrderedDict([
        # Costumes that can be used in lives. Usually associated with cards but
        # they aren't always (e.g. Year of the Dog)
        ('live', _('Live')),
        # Never associated with cards.
        ('other', _('Other')),
    ])
    i_costume_type = models.PositiveIntegerField(_('Costume type'), choices=i_choices(COSTUME_TYPE_CHOICES))

    # Basically whatever you want. If there's a card associated with a model, we'll use the
    # card's title instead.
    name = models.CharField(_('Name'), max_length=250, null=True)
    NAMES_CHOICES = ALL_ALT_LANGUAGES
    d_names = models.TextField(_('Name'), null=True)

    @property
    def t_name(self):
        # If we're a card costume, take that card's title so we don't have to save/TL duplicate strings.
        # The form will make sure self.name is null.
        if self.card:
            return self.card.t_name or self.card.japanese_name
        return self.names.get(get_language(), self.name)

    _tthumbnail_image = models.ImageField(null=True, upload_to=uploadTthumb('cos/z'))
    image = models.ImageField(_('Image'), upload_to=uploadItem('cos/p'), null=True)
    model_pkg = models.FileField(pgettext_lazy('BanPa model viewer', 'Model'), upload_to=uploadItem('cos/z'), null=True)

    @property
    def display_image(self):
        if self.image:
            return self.image_url
        elif self.card:
            for try_img in ['transparent_trained_url', 'transparent_url']:
                g = getattr(self.card, try_img, None)
                if g:
                    return g
        return None

    @property
    def display_image_thumbnail_url(self):
        if self.image:
            return self.image_thumbnail_url
        elif self.card:
            for try_img in ['transparent_trained_thumbnail_url', 'transparent_thumbnail_url']:
                g = getattr(self.card, try_img, None)
                if g:
                    return g
        return None

    # there's nothing stopping you from associating a costume with a card whose member is
    # different, but it's weird so keep it in sync elsewhere (forms.py)
    # additionally, this is nullable just in case we want to upload NPC costumes.
    member = models.ForeignKey(Member, verbose_name=_('Member'), related_name='associated_costume', null=True, on_delete=models.CASCADE)
    card = models.OneToOneField(Card, verbose_name=_('Card'), related_name='associated_costume', null=True, on_delete=models.SET_NULL)
    # owned_chibis

    def __unicode__(self):
        return u'{}{}'.format(
            u'{} - '.format(self.member.t_name) if self.member_id else '',
            self.t_name,
        )
    
    # Cache chibis

    _cache_chibis_days = 200
    _cache_chibis_last_update = models.DateTimeField(null=True)
    _cache_chibis_ids = models.TextField(null=True)
    _cache_chibis_paths = models.TextField(null=True)

    def update_cache_chibis(self, chibis=None):
        self._cache_chibis_last_update = timezone.now()
        if not chibis:
            chibis = Chibi.objects.filter(costume=self)
        self._cache_chibis_ids = join_data(*[ image.id for image in chibis ])
        self._cache_chibis_paths = join_data(*[ unicode(image) for image in chibis ])

    def force_cache_chibis(self):
        self.update_cache_chibis()
        self.save()

    @property
    def cached_chibis(self):
        if not self._cache_chibis_last_update or self._cache_chibis_last_update < timezone.now() - datetime.timedelta(days=self._cache_chibis_days):
            self.force_cache_chibis()
        if not self._cache_chibis_ids:
            return []
        return [AttrDict({
            'id': id,
            'pk': id,
            'image': path,
            'image_url': get_image_url_from_path(path),
            'http_image_url': get_http_image_url_from_path(path),
        }) for id, path in zip(split_data(self._cache_chibis_ids), split_data(self._cache_chibis_paths))]
