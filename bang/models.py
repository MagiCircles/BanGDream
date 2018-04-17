# -*- coding: utf-8 -*-
from __future__ import division
import datetime, time
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.db.models import Q
from django.db import models
from django.conf import settings as django_settings
from magi.models import User, uploadItem
from magi.abstract_models import AccountAsOwnerModel, BaseAccount
from magi.item_model import BaseMagiModel, MagiModel, get_image_url_from_path, get_http_image_url_from_path, i_choices, getInfoFromChoices
from magi.utils import AttrDict, tourldash, split_data, join_data, uploadToKeepName, staticImageURL
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

class Image(BaseMagiModel):
    image = models.ImageField(upload_to=uploadToKeepName('images/'))

    def __unicode__(self):
        return unicode(self.image)

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
        }),
        ('EN', {
            'translation': _('English version'),
            'image': 'world',
            'prefix': 'english_',
            'code': 'en',
        }),
        ('TW', {
            'translation': _('Taiwanese version'),
            'image': 'zh-hant',
            'prefix': 'taiwanese_',
            'code': 'zh-hant',
        }),
        ('KR', {
            'translation': _('Korean version'),
            'image': 'kr',
            'prefix': 'korean_',
            'code': 'kr',
        }),
    ])
    VERSION_CHOICES = [(_name, _info['translation']) for _name, _info in VERSIONS.items()]
    VERSIONS_PREFIXES = OrderedDict([(_k, _v['prefix']) for _k, _v in VERSIONS.items()])
    i_version = models.PositiveIntegerField(_('Version'), choices=i_choices(VERSION_CHOICES))
    version_image = property(getInfoFromChoices('version', VERSIONS, 'image'))
    version_image_url = property(lambda _a: staticImageURL(_a.version_image, folder=u'language', extension='png'))

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
    os_icon = property(lambda _a: _a.os)

    device = models.CharField(_('Device'), help_text=_('The model of your device. Example: Nexus 5, iPhone 4, iPad 2, ...'), max_length=150, null=True)
    stargems_bought = models.PositiveIntegerField(null=True)

    screenshot = models.ImageField(_('Screenshot'), help_text=_('In-game profile screenshot'), upload_to=uploadItem('account_screenshot'), null=True)

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
    def t_name(self):
        if get_language() == 'ja':
            return self.japanese_name
        return self.names.get(get_language(), self.name)

    image = models.ImageField(_('Image'), upload_to=uploadItem('i'))
    square_image = models.ImageField(_('Image'), upload_to=uploadItem('i/m'))

    BAND_CHOICES = (
        'Poppin\' Party',
        'Afterglow',
        'Pastel*Palettes',
        'Roselia',
        'Hello, Happy World!',
        'Glitter*Green'
    )
    i_band = models.PositiveIntegerField(_('Band'), choices=i_choices(BAND_CHOICES))

    school = models.CharField(_('School'), max_length=100, null=True)
    SCHOOLS_CHOICES = ALL_ALT_LANGUAGES
    d_schools = models.TextField(_('School'), null=True)

    SCHOOL_YEAR_CHOICES = (
        ('First', _('First')),
        ('Second', _('Second')),
        ('Third', _('Junior Third')),
    )
    i_school_year = models.PositiveIntegerField(_('School Year'), choices=i_choices(SCHOOL_YEAR_CHOICES), null=True)

    # TODO: separate page of voice acctresses
    romaji_CV = models.CharField(_('CV'), help_text='In romaji.', max_length=100, null=True)
    CV = models.CharField(string_concat(_('CV'), ' (', t['Japanese'], ')'), help_text='In Japanese characters.', max_length=100, null=True)

    birthday = models.DateField(_('Birthday'), null=True, help_text='The year is not used, so write whatever')

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

    description = models.TextField(_('Description'), null=True)
    DESCRIPTIONS_CHOICES = ALL_ALT_LANGUAGES
    d_descriptions = models.TextField(_('Description'), null=True)

    reverse_related = (
        ('cards', 'cards', _('Cards')),
        ('fans', 'accounts', _('Fans')),
    )

    # Cache totals
    _cache_totals_days = 1
    _cache_totals_last_update = models.DateTimeField(null=True)
    _cache_total_fans = models.PositiveIntegerField(null=True)
    _cache_total_cards = models.PositiveIntegerField(null=True)

    def update_cache_totals(self):
        self._cache_totals_last_update = timezone.now()
        self._cache_total_fans = User.objects.filter(
            Q(preferences__favorite_character1=self.id)
            | Q(preferences__favorite_character2=self.id)
            | Q(preferences__favorite_character3=self.id)
        ).count()
        self._cache_total_cards = Card.objects.filter(member=self).count()

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
            return self.japanese_name
        return self.names.get(get_language(), self.name)

    VERSIONS_CHOICES = Account.VERSION_CHOICES
    c_versions = models.TextField(_('Server availability'), blank=True, null=True, default='"JP"')

    release_date = models.DateField(_('Release date'), null=True, db_index=True)
    is_promo = models.BooleanField(_('Promo card'), default=False)

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
                'based_on_stamina': _(u'For the next {duration} seconds, if life is above {stamina}, score boosted by +{percentage}%, otherwise, score boosted by +{alt_percentage}%'),
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
    image = models.ImageField(_('Icon'), upload_to=uploadItem('c'), null=True)
    image_trained = models.ImageField(string_concat(_('Icon'), ' (', _('Trained'), ')'), upload_to=uploadItem('c/a'), null=True)
    art = models.ImageField(_('Art'), upload_to=uploadItem('c/art'), null=True)
    art_trained = models.ImageField(string_concat(_('Art'), ' (', _('Trained'), ')'), upload_to=uploadItem('c/art/a'), null=True)
    transparent = models.ImageField(_('Transparent'), upload_to=uploadItem('c/transparent'), null=True)
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

    # Chibi images

    chibis = models.ManyToManyField(Image, related_name="chibi", verbose_name=_('Chibi'))

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
                    (getattr(self, field + '_' + status) / django_settings.MAX_STATS[field + '_' + ('trained_max' if self.trainable else 'max')]) * 100,
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
            'image': unicode(self.member.image),
        }

    # Cache events

    _cached_events_collection_name = 'event'
    _cache_events_days = 20
    _cache_events_last_update = models.DateTimeField(null=True)
    _cache_j_events = models.TextField(null=True)

    @classmethod
    def cached_events_pre(self, d):
        d['unicode'] = d['japanese_name'] if get_language() == 'ja' else d['name']
        return d

    def to_cache_events(self):
        events = []
        for event in Event.objects.filter(Q(main_card_id=self.id) | Q(secondary_card_id=self.id)):
            events.append({
                'id': event.id,
                'name': event.name,
                'japanese_name': event.japanese_name,
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
        d['unicode'] = d['japanese_name'] if get_language() == 'ja' else d['name']
        return d

    def to_cache_gachas(self):
        gachas = []
        for gacha in Gacha.objects.filter(cards__id=self.id):
            gachas.append({
                'id': gacha.id,
                'name': gacha.name,
                'japanese_name': gacha.japanese_name,
                'image': unicode(gacha.image),
            })
        return gachas if gachas else None

    # Cache chibis

    _cache_chibis_days = 200
    _cache_chibis_last_update = models.DateTimeField(null=True)
    _cache_chibis_ids = models.TextField(null=True)
    _cache_chibis_paths = models.TextField(null=True)

    def update_cache_chibis(self, chibis=None):
        self._cache_chibis_last_update = timezone.now()
        if not chibis:
            chibis = self.chibis.all()
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

    @property # To allow favorite card to use the same template
    def card(self):
        return self

    def __unicode__(self):
        if self.id:
            return u'{rarity} {member_name} - {attribute}{name}'.format(
                rarity=self.t_rarity,
                member_name=self.cached_member.t_name if self.cached_member else '',
                attribute=self.t_attribute,
                name=(u' - {}'.format(
                    self.japanese_name
                    if (get_language() == 'ja' and self.japanese_name) or not self.name
                    else self.name) if self.name or self.japanese_name else ''),
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
    def color(self):
        return self.card.english_attribute

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
        ('band_battle', _('Band Battle')),
        ('live_trial', _('Live Trial')),
    )
    i_type = models.PositiveIntegerField(_('Event type'), choices=i_choices(TYPE_CHOICES), default=0)

    SONG_RANKING_TYPES = [
        'challenge_live',
        'band_battle',
    ]
    TRIAL_MASTER_TYPES = [
        'live_trial',
    ]

    rare_stamp = models.ImageField(_('Rare stamp'), upload_to=uploadItem('e/stamps'), null=True)
    @property
    def rare_stamp_per_version(self):
        return _event_gacha_top_image(self, image_name='rare_stamp')

    stamp_translation = models.CharField(_('Stamp translation'), max_length=200, null=True)
    STAMP_TRANSLATIONS_CHOICES = ALT_LANGUAGES_EXCEPT_JP
    d_stamp_translations = models.TextField(_('Stamp translation'), null=True)

    @property
    def t_stamp_translation(self):
        if get_language() == 'ja':
            return None
        return self.stamp_translations.get(get_language(), self.stamp_translation)

    start_date = models.DateTimeField(string_concat(_('Japanese version'), ' - ', _('Beginning')), null=True)
    end_date = models.DateTimeField(string_concat(_('Japanese version'), ' - ',_('End')), null=True)

    FIELDS_PER_VERSION = ['image', 'countdown', 'start_date', 'end_date', 'rare_stamp', 'stamp_translation']

    VERSIONS_CHOICES = Account.VERSION_CHOICES
    c_versions = models.TextField(_('Server availability'), blank=True, null=True, default='"JP"')

    english_image = models.ImageField(string_concat(_('English version'), ' - ', _('Image')), upload_to=uploadItem('e/e'), null=True)
    english_start_date = models.DateTimeField(string_concat(_('English version'), ' - ', _('Beginning')), null=True)
    english_end_date = models.DateTimeField(string_concat(_('English version'), ' - ', _('End')), null=True)
    english_rare_stamp = models.ImageField(string_concat(_('English version'), ' - ', _('Rare stamp')), upload_to=uploadItem('e/stamps/en'), null=True)

    taiwanese_image = models.ImageField(string_concat(_('Taiwanese version'), ' - ', _('Image')), upload_to=uploadItem('e/t'),  null=True)
    taiwanese_start_date = models.DateTimeField(string_concat(_('Taiwanese version'), ' - ', _('Beginning')), null=True)
    taiwanese_end_date = models.DateTimeField(string_concat(_('Taiwanese version'), ' - ', _('End')), null=True)
    taiwanese_rare_stamp = models.ImageField(string_concat(_('Taiwanese version'), ' - ', _('Rare stamp')), upload_to=uploadItem('e/stamps/tw'), null=True)

    korean_image = models.ImageField(string_concat(_('Korean version'), ' - ', _('Image')), upload_to=uploadItem('e/t'),  null=True)
    korean_start_date = models.DateTimeField(string_concat(_('Korean version'), ' - ', _('Beginning')), null=True)
    korean_end_date = models.DateTimeField(string_concat(_('Korean version'), ' - ', _('End')), null=True)
    korean_rare_stamp = models.ImageField(string_concat(_('Korean version'), ' - ', _('Rare stamp')), upload_to=uploadItem('e/stamps/kr'), null=True)

    main_card = models.ForeignKey(Card, related_name='main_card_event', null=True, limit_choices_to={
        'i_rarity': 3,
    }, on_delete=models.SET_NULL)
    secondary_card = models.ForeignKey(Card, related_name='secondary_card_event', null=True, limit_choices_to={
        'i_rarity': 2,
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
        if not end_date or not start_date:
            return None
        now = timezone.now()
        if now > end_date:
            return 'ended'
        elif now > start_date:
            return 'current'
        return 'future'

    status = property(lambda _s: _s.get_status())
    english_status = property(lambda _s: _s.get_status(version='EN'))
    taiwanese_status = property(lambda _s: _s.get_status(version='TW'))
    korean_status = property(lambda _s: _s.get_status(version='KR'))

    def __unicode__(self):
        return unicode(self.japanese_name if get_language() == 'ja' and self.japanese_name else self.name)

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

    screenshot = models.ImageField(_('Screenshot'), upload_to=uploadItem('event_screenshot'), null=True)

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
        MaxValueValidator(28),
    ]

    DIFFICULTIES = [
        ('easy', _('Easy')),
        ('normal', _('Normal')),
        ('hard', _('Hard')),
        ('expert', _('Expert')),
    ]

    SONGWRITERS_DETAILS = [
        ('composer', _('Composer')),
        ('lyricist', _('Lyricist')),
        ('arranger', _('Arranger')),
    ]

    owner = models.ForeignKey(User, related_name='added_songs')
    image = models.ImageField('Album cover', upload_to=uploadItem('s'))

    BAND_CHOICES = Member.BAND_CHOICES
    i_band = models.PositiveIntegerField(_('Band'), choices=i_choices(BAND_CHOICES))

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

    def __unicode__(self):
        return self.romaji_name if self.romaji_name and get_language() != 'ja'  else self.japanese_name

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
    )

    i_difficulty = models.PositiveIntegerField(_('Difficulty'), choices=i_choices(DIFFICULTY_CHOICES), default=0)
    difficulty_image_url = property(lambda _ps: staticImageURL(_ps.difficulty, folder=u'songs', extension='png'))

    score = models.PositiveIntegerField(_('Score'), null=True)
    full_combo = models.NullBooleanField(_('Full combo'))

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

    def __unicode__(self):
        if self.id:
            return unicode(self.song)
        return super(PlayedSong, self).__unicode__()

############################################################
# Gacha

class Gacha(MagiModel):
    collection_name = 'gacha'

    owner = models.ForeignKey(User, related_name='added_gacha')

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

    start_date = models.DateTimeField(_('Beginning'), null=True)
    end_date = models.DateTimeField(_('End'), null=True)

    english_image = models.ImageField(string_concat(_('English version'), ' - ', _('Image')), upload_to=uploadItem('e/e'), null=True)
    english_start_date = models.DateTimeField(string_concat(_('English version'), ' - ', _('Beginning')), null=True)
    english_end_date = models.DateTimeField(string_concat(_('English version'), ' - ', _('End')), null=True)

    taiwanese_image = models.ImageField(string_concat(_('Taiwanese version'), ' - ', _('Image')), upload_to=uploadItem('e/t'), null=True)
    taiwanese_start_date = models.DateTimeField(string_concat(_('Taiwanese version'), ' - ', _('Beginning')), null=True)
    taiwanese_end_date = models.DateTimeField(string_concat(_('Taiwanese version'), ' - ', _('End')), null=True)

    korean_image = models.ImageField(string_concat(_('Korean version'), ' - ', _('Image')), upload_to=uploadItem('e/t'), null=True)
    korean_start_date = models.DateTimeField(string_concat(_('Korean version'), ' - ', _('Beginning')), null=True)
    korean_end_date = models.DateTimeField(string_concat(_('Korean version'), ' - ', _('End')), null=True)

    ATTRIBUTE_CHOICES = Card.ATTRIBUTE_CHOICES
    ATTRIBUTE_WITHOUT_I_CHOICES = True
    i_attribute = models.PositiveIntegerField(_('Attribute'), choices=ATTRIBUTE_CHOICES, null=True)
    english_attribute = property(getInfoFromChoices('attribute', Card.ATTRIBUTES, 'english'))

    event = models.ForeignKey(Event, verbose_name=_('Event'), related_name='gachas', null=True, on_delete=models.SET_NULL)
    cards = models.ManyToManyField(Card, verbose_name=('Cards'), related_name='gachas')

    FIELDS_PER_VERSION = ['image', 'countdown', 'start_date', 'end_date']

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
        if not end_date or not start_date:
            return None
        now = timezone.now()
        if now > end_date:
            return 'ended'
        elif now > start_date:
            return 'current'
        return 'future'

    status = property(lambda _s: _s.get_status())
    english_status = property(lambda _s: _s.get_status(version='EN'))
    taiwanese_status = property(lambda _s: _s.get_status(version='TW'))
    korean_status = property(lambda _s: _s.get_status(version='KR'))

    def __unicode__(self):
        return unicode(self.japanese_name if get_language() == 'ja' and self.japanese_name else self.name)
