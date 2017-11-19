# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _, string_concat

############################################################
# Members

BANDS = [
    'Poppin\' Party',
    'Afterglow',
    'Pastel*Palettes',
    'Roselia',
    'Hello, Happy World!',
]

BAND_CHOICES = list(enumerate(BANDS))
BAND_DICT = dict(BAND_CHOICES)

ENGLISH_ASTROLOGICAL_SIGNS = [
    'Leo',
    'Aries',
    'Libra',
    'Virgo',
    'Scorpio',
    'Capricorn',
    'Pisces',
    'Gemini',
    'Cancer',
    'Sagittarius',
    'Aquarius',
    'Taurus',
]
ENGLISH_ASTROLOGICAL_SIGN_CHOICES = list(enumerate(ENGLISH_ASTROLOGICAL_SIGNS))
ENGLISH_ASTROLOGICAL_SIGN_DICT = dict(ENGLISH_ASTROLOGICAL_SIGN_CHOICES)
ASTROLOGICAL_SIGN_REVERSE_DICT = { value: key for (key, value) in list(enumerate(ENGLISH_ASTROLOGICAL_SIGNS)) }
ASTROLOGICAL_SIGNS = [
    _('Leo'),
    _('Aries'),
    _('Libra'),
    _('Virgo'),
    _('Scorpio'),
    _('Capricorn'),
    _('Pisces'),
    _('Gemini'),
    _('Cancer'),
    _('Sagittarius'),
    _('Aquarius'),
    _('Taurus'),
]
ASTROLOGICAL_SIGN_CHOICES = list(enumerate(ASTROLOGICAL_SIGNS))
ASTROLOGICAL_SIGN_DICT = dict(ASTROLOGICAL_SIGN_CHOICES)

SCHOOL_YEARS = [
    _('First'),
    _('Second'),
    _('Junior Third'),
]

ENGLISH_SCHOOL_YEARS = [
    'First',
    'Second',
    'Third',
]

SCHOOL_YEAR_CHOICES = list(enumerate(SCHOOL_YEARS))
SCHOOL_YEAR_DICT = dict(SCHOOL_YEAR_CHOICES)

ENGLISH_SCHOOL_YEAR_CHOICES = list(enumerate(ENGLISH_SCHOOL_YEARS))
ENGLISH_SCHOOL_YEAR_DICT = dict(ENGLISH_SCHOOL_YEAR_CHOICES)

############################################################
# Cards

RARITY_1 = 1
RARITY_2 = 2
RARITY_3 = 3
RARITY_4 = 4

RARITY_CHOICES = [
    (RARITY_1, u'★'),
    (RARITY_2, u'★★'),
    (RARITY_3, u'★★★'),
    (RARITY_4, u'★★★★'),
]
RARITY_DICT = dict(RARITY_CHOICES)

TRAINABLE_RARITIES = [RARITY_3, RARITY_4]

MAX_LEVELS = {
    RARITY_1: 20,
    RARITY_2: 30,
    RARITY_3: (40, 50),
    RARITY_4: (50, 60),
}

ATTRIBUTE_POWER = 1
ATTRIBUTE_COOL = 2
ATTRIBUTE_PURE = 3
ATTRIBUTE_HAPPY = 4

ATTRIBUTE_CHOICES = [
    (ATTRIBUTE_POWER, _('Power')),
    (ATTRIBUTE_COOL, _('Cool')),
    (ATTRIBUTE_PURE, _('Pure')),
    (ATTRIBUTE_HAPPY, _('Happy')),
]
ATTRIBUTE_DICT = dict(ATTRIBUTE_CHOICES)

ENGLISH_ATTRIBUTE_CHOICES = [
    (ATTRIBUTE_POWER, 'Power'),
    (ATTRIBUTE_COOL, 'Cool'),
    (ATTRIBUTE_PURE, 'Pure'),
    (ATTRIBUTE_HAPPY, 'Happy'),
]
ENGLISH_ATTRIBUTE_DICT = dict(ENGLISH_ATTRIBUTE_CHOICES)

SKILL_SCORE_UP = 1
SKILL_LIFE_RECOVERY = 2
SKILL_PERFECT_LOCK = 3

ENGLISH_SKILL_TYPES_DICT = {
    SKILL_SCORE_UP: 'Score Up',
    SKILL_LIFE_RECOVERY: 'Life Recovery',
    SKILL_PERFECT_LOCK: 'Perfect Lock',
}

SKILL_TYPES = {
    SKILL_SCORE_UP: (_('Score Up'), u'スコアＵＰ'),
    SKILL_LIFE_RECOVERY: (_('Life Recovery'), u'ライフ回復'),
    SKILL_PERFECT_LOCK: (_('Perfect Lock'), u'判定強化'),
}

SKILL_TYPE_CHOICES = [ (value, info[0]) for (value, info) in SKILL_TYPES.items() ]
SKILL_TYPE_DICT = dict(SKILL_TYPE_CHOICES)
JAPANESE_SKILL_TYPE_CHOICES = [ (value, info[1]) for (value, info) in SKILL_TYPES.items() ]
JAPANESE_SKILL_TYPE_DICT = dict(JAPANESE_SKILL_TYPE_CHOICES)

SKILL_SIZES = {
    RARITY_1: (_(u'small'), u'小', u''),
    RARITY_2: (_(u'medium'), u'中', u'GREAT'),
    RARITY_3: (_(u'large'), u'大', u'GOOD'),
    RARITY_4: (_(u'oversized'), u'特大', u'BAD'),
}

SKILL_SIZE_DICT = { value: info[0] for (value, info) in SKILL_SIZES.items() }
JAPANESE_SKILL_SIZE_DICT = { value: info[1] for (value, info) in SKILL_SIZES.items() }

SKILL_TEMPLATES = {
    SKILL_SCORE_UP: _(u'All notes will receive a {size} score bonus.'),
    SKILL_LIFE_RECOVERY: _(u'Your life will get a {size} boost.'),
    SKILL_PERFECT_LOCK: _(u'All the {note_type} notes or better will turn into PERFECT.'),
}

JAPANESE_SKILL_TEMPLATES = {
    SKILL_SCORE_UP: u'スコアが{size}UPする',
    SKILL_LIFE_RECOVERY: u'ライフが{size}回復する',
    SKILL_PERFECT_LOCK: u'5秒間{note_type}以上がすべてPERFECTになる',
}

SKILL_ICONS = {
    SKILL_SCORE_UP: 'scoreup',
    SKILL_LIFE_RECOVERY: 'healer',
    SKILL_PERFECT_LOCK: 'perfectlock',
}

############################################################
# Songs

UNLOCK = [
    ('gift', _('Gift')),
    ('purchase', _('Purchase at CiRCLE')),
    ('complete_story', _('Complete story')),
    ('complete_tutorial', _('Complete Tutorial')),
    ('initial', _('Initially available')),
    ('event', _('Event gift')),
    ('other', _('Other')),
]

UNLOCK_CHOICES = list(enumerate([u[1] for u in UNLOCK]))
UNLOCK_DICT = { i: u[0] for i, u in enumerate(UNLOCK) }

UNLOCK_SENTENCES = {
    'gift': string_concat(_('Gift'), ' ({occasion})'),
    'purchase': _('Purchase at CiRCLE'),
    'complete_story': _('Complete {story_type} story, chapter {chapter}'),
    'complete_tutorial': _('Complete Tutorial'),
    'initial': _('Initially available'),
    'event': _('Event gift'),
    'other': '{how_to_unlock}',
}

UNLOCK_VARIABLES = {
    'gift': ['occasion'],
    'purchase': [],
    'complete_story': ['story_type', 'chapter'],
    'complete_tutorial': [],
    'initial': [],
    'event': [],
    'other': ['how_to_unlock'],
}
