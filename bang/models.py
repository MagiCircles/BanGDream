# -*- coding: utf-8 -*-
from __future__ import division
import datetime, time
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.db.models import Q
from django.db import models
from django.conf import settings as django_settings
from web.models import User, uploadItem
from web.item_model import ItemModel, get_image_url_from_path, get_http_image_url_from_path
from web.utils import AttrDict, tourldash, split_data
from bang.model_choices import *
from bang.django_translated import t

############################################################
# Account

class Account(ItemModel):
    collection_name = 'account'

    owner = models.ForeignKey(User, related_name='accounts')
    creation = models.DateTimeField(_('Join Date'), auto_now_add=True)
    start_date = models.DateField(_('Start Date'), null=True)
    level = models.PositiveIntegerField(_("Level"), null=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(300),
    ])
    friend_id = models.PositiveIntegerField(_('Friend ID'), null=True)

    @property
    def item_url(self):
        return self.owner.item_url

    @property
    def full_item_url(self):
        return self.owner.full_item_url

    @property
    def http_item_url(self):
        return self.owner.http_item_url

    def __unicode__(self):
        return u'#{} Level {}'.format(self.id, self.level)

############################################################
# Members

class Member(ItemModel):
    collection_name = 'member'

    owner = models.ForeignKey(User, related_name='added_members')
    name = models.CharField(string_concat(_('Name'), ' (romaji)'), max_length=100, unique=True)
    japanese_name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100, null=True)
    image = models.ImageField(_('Image'), upload_to=uploadItem('i'))
    square_image = models.ImageField(_('Image'), upload_to=uploadItem('i/m'))
    @property
    def square_image_url(self): return get_image_url_from_path(self.square_image)
    @property
    def http_square_image_url(self): return get_http_image_url_from_path(self.square_image)

    i_band = models.PositiveIntegerField(_('Band'), choices=BAND_CHOICES)
    @property
    def band(self): return BAND_DICT[self.i_band]

    school = models.CharField(_('School'), max_length=100, null=True)
    i_school_year = models.PositiveIntegerField(_('School Year'), choices=SCHOOL_YEAR_CHOICES, null=True)
    @property
    def school_year(self): return SCHOOL_YEAR_DICT[self.i_school_year] if self.i_school_year is not None else None

    romaji_CV = models.CharField(_('CV'), help_text='In romaji.', max_length=100, null=True)
    CV = models.CharField(string_concat(_('CV'), ' (', t['Japanese'], ')'), help_text='In Japanese characters.', max_length=100, null=True)

    birthday = models.DateField(_('Birthday'), null=True, help_text='The year is not used, so write whatever')
    food_likes = models.CharField(_('Liked food'), max_length=100, null=True)
    food_dislikes = models.CharField(_('Disliked food'), max_length=100, null=True)

    i_astrological_sign = models.PositiveIntegerField(_('Astrological Sign'), choices=ASTROLOGICAL_SIGN_CHOICES, null=True)
    @property
    def astrological_sign(self): return ASTROLOGICAL_SIGN_DICT[self.i_astrological_sign] if self.i_astrological_sign is not None else None
    @property
    def english_astrological_sign(self): return ENGLISH_ASTROLOGICAL_SIGN_DICT[self.i_astrological_sign] if self.i_astrological_sign is not None else None
    @property
    def astrological_sign_image_url(self): return get_image_url_from_path(u'static/img/i_astrological_sign/{}.png'.format(self.i_astrological_sign))

    hobbies = models.CharField(_('Instrument'), max_length=100, null=True)
    description = models.TextField(_('Description'), null=True)

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
        return unicode(self.japanese_name if get_language() == 'ja' and self.japanese_name else self.name)

############################################################
# Card

class Card(ItemModel):
    collection_name = 'card'

    owner = models.ForeignKey(User, related_name='added_cards')
    id = models.PositiveIntegerField(_('ID'), unique=True, primary_key=True, db_index=True)
    member = models.ForeignKey(Member, verbose_name=_('Member'), related_name='cards', null=True, on_delete=models.SET_NULL)

    i_rarity = models.PositiveIntegerField(_('Rarity'), choices=RARITY_CHOICES)
    @property
    def rarity(self): return RARITY_DICT[self.i_rarity]
    i_attribute = models.PositiveIntegerField(_('Attribute'), choices=ATTRIBUTE_CHOICES)
    @property
    def attribute(self): return ATTRIBUTE_DICT[self.i_attribute]
    @property
    def english_attribute(self): return ENGLISH_ATTRIBUTE_DICT[self.i_attribute]

    name = models.CharField(_('Title'), max_length=100, null=True)
    japanese_name = models.CharField(string_concat(_('Title'), ' (', t['Japanese'], ')'), max_length=100, null=True)

    # Images
    image = models.ImageField(_('Icon'), upload_to=uploadItem('c'))
    image_trained = models.ImageField(string_concat(_('Icon'), ' (', _('Trained'), ')'), upload_to=uploadItem('c/a'))
    @property
    def image_trained_url(self): return get_image_url_from_path(self.image_trained)
    @property
    def http_image_trained_url(self): return get_http_image_url_from_path(self.image_trained)
    art = models.ImageField(_('Art'), upload_to=uploadItem('c/art'))
    @property
    def art_url(self): return get_image_url_from_path(self.art)
    @property
    def http_art_url(self): return get_http_image_url_from_path(self.art)
    art_trained = models.ImageField(string_concat(_('Art'), ' (', _('Trained'), ')'), upload_to=uploadItem('c/art/a'))
    @property
    def art_trained_url(self): return get_image_url_from_path(self.art_trained)
    @property
    def http_art_trained_url(self): return get_http_image_url_from_path(self.art_trained)
    transparent = models.ImageField(_('Transparent'), upload_to=uploadItem('c/transparent'))
    @property
    def transparent_url(self): return get_image_url_from_path(self.transparent)
    @property
    def http_transparent_url(self): return get_http_image_url_from_path(self.transparent)
    transparent_trained = models.ImageField(string_concat(_('Transparent'), ' (', _('Trained'), ')'), upload_to=uploadItem('c/transparent/a'))
    @property
    def transparent_trained_url(self): return get_image_url_from_path(self.transparent_trained)
    @property
    def http_transparent_trained_url(self): return get_http_image_url_from_path(self.transparent_trained)
    chibi = models.ImageField(_('Chibi'), upload_to=uploadItem('c/c'), null=True)
    @property
    def chibi_url(self): return get_image_url_from_path(self.chibi)
    @property
    def http_chibi_url(self): return get_http_image_url_from_path(self.chibi)

    # Skill

    i_skill_type = models.PositiveIntegerField(_('Skill'), choices=SKILL_TYPE_CHOICES)
    @property
    def skill_type(self): return SKILL_TYPE_DICT[self.i_skill_type]
    @property
    def japanese_skill_type(self): return JAPANESE_SKILL_TYPE_DICT[self.i_skill_type]
    skill_name = models.CharField(_('Skill name'), max_length=100, null=True)
    japanese_skill_name = models.CharField(string_concat(_('Skill name'), ' (', t['Japanese'], ')'), max_length=100, null=True)
    skill_details = models.CharField(_('Skill'), max_length=500, null=True)

    @property
    def skill(self):
        return self.skill_details or SKILL_TEMPLATES[self.i_skill_type].format(size=SKILL_SIZES[self.i_rarity][0], note_type=SKILL_SIZES[self.i_rarity][2])

    @property
    def japanese_skill(self):
        return JAPANESE_SKILL_TEMPLATES[self.i_skill_type].format(size=SKILL_SIZES[self.i_rarity][1], note_type=SKILL_SIZES[self.i_rarity][2])

    # Side skill

    i_side_skill_type = models.PositiveIntegerField(_('Side skill'), choices=SKILL_TYPE_CHOICES, null=True)
    @property
    def side_skill_type(self): return SKILL_TYPE_DICT[self.i_side_skill_type]
    @property
    def japanese_side_skill_type(self): return JAPANESE_SKILL_TYPE_DICT[self.i_side_skill_type]
    side_skill_details = models.CharField(_('Side skill'), max_length=500, null=True)

    @property
    def side_skill(self):
        return self.side_skill_details or SKILL_TEMPLATES[self.i_side_skill_type].format(size=SKILL_SIZES[self.i_rarity][0], note_type=SKILL_SIZES[self.i_rarity][2])

    @property
    def japanese_side_skill(self):
        return JAPANESE_SKILL_TEMPLATES[self.i_side_skill_type].format(size=SKILL_SIZES[self.i_rarity][1], note_type=SKILL_SIZES[self.i_rarity][2])

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

    # Tools

    @property
    def trainable(self):
        return self.i_rarity in TRAINABLE_RARITIES

    @property
    def max_level(self):
        return MAX_LEVELS[self.i_rarity][0] if self.trainable else MAX_LEVELS[self.i_rarity]

    @property
    def max_level_trained(self):
        return MAX_LEVELS[self.i_rarity][1] if self.trainable else MAX_LEVELS[self.i_rarity]

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
                    (getattr(self, field + '_' + status) / django_settings.MAX_STATS[field + '_max']) * 100,
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
    _cache_member_name = models.CharField(max_length=100, null=True)
    _cache_member_japanese_name = models.CharField(max_length=100, null=True)
    _cache_member_image = models.ImageField(upload_to=uploadItem('member'), null=True)

    def update_cache_member(self):
        self._cache_member_last_update = timezone.now()
        if self.member_id:
            self._cache_member_name = self.member.name
            self._cache_member_japanese_name = self.member.japanese_name
            self._cache_member_image = self.member.image

    def force_cache_member(self):
        self.update_cache_member()
        self.save()

    @property
    def cached_member(self):
        if not self._cache_member_last_update or self._cache_member_last_update < timezone.now() - datetime.timedelta(days=self._cache_member_days):
            self.force_cache_member()
        return AttrDict({
            'pk': self.member_id,
            'id': self.member_id,
            'unicode': self._cache_member_name if get_language() != 'ja' else self._cache_member_japanese_name,
            'name': self._cache_member_name,
            'japanese_name': self._cache_member_japanese_name,
            'image': self._cache_member_image,
            'image_url': get_image_url_from_path(self._cache_member_image),
            'http_image_url': get_http_image_url_from_path(self._cache_member_image),
            'item_url': u'/member/{}/{}/'.format(self.member_id, tourldash(self._cache_member_name)) if self.member_id else '#',
            'ajax_item_url': u'/ajax/member/{}/'.format(self.member_id) if self.member_id else '',
        })

    # Cache event

    _cache_event_days = 20
    _cache_event_last_update = models.DateTimeField(null=True)
    _cache_event_id = models.PositiveIntegerField(null=True)
    _cache_event_name = models.CharField(max_length=100, null=True)
    _cache_event_japanese_name = models.CharField(max_length=100, null=True)
    _cache_event_image = models.ImageField(upload_to=uploadItem('e'), null=True)

    def update_cache_event(self):
        self._cache_event_last_update = timezone.now()
        try:
            event = Event.objects.filter(Q(main_card_id=self.id) | Q(secondary_card_id=self.id))[0]
        except IndexError:
            event = None
        if event:
            self._cache_event_id = event.id
            self._cache_event_name = event.name
            self._cache_event_japanese_name = event.japanese_name
            self._cache_event_image = event.image
        else:
            self._cache_event_id = None

    def force_cache_event(self):
        self.update_cache_event()
        self.save()

    @property
    def cached_event(self):
        if not self._cache_event_last_update or self._cache_event_last_update < timezone.now() - datetime.timedelta(days=self._cache_event_days):
            self.force_cache_event()
        if not self._cache_event_id:
            return None
        return AttrDict({
            'pk': self._cache_event_id,
            'id': self._cache_event_id,
            'unicode': self._cache_event_name if get_language() != 'ja' else self._cache_event_japanese_name,
            'name': self._cache_event_name,
            'japanese_name': self._cache_event_japanese_name,
            'image': self._cache_event_image,
            'image_url': get_image_url_from_path(self._cache_event_image),
            'http_image_url': get_http_image_url_from_path(self._cache_event_image),
            'item_url': u'/event/{}/{}/'.format(self._cache_event_id, tourldash(self._cache_event_name)),
            'ajax_item_url': u'/ajax/event/{}/'.format(self._cache_event_id),
        })

    # Cache gacha

    _cache_gacha_days = 20
    _cache_gacha_last_update = models.DateTimeField(null=True)
    _cache_gacha_id = models.PositiveIntegerField(null=True)
    _cache_gacha_name = models.CharField(max_length=100, null=True)
    _cache_gacha_japanese_name = models.CharField(max_length=100, null=True)
    _cache_gacha_image = models.ImageField(upload_to=uploadItem('e'), null=True)

    def update_cache_gacha(self):
        self._cache_gacha_last_update = timezone.now()
        try:
            gacha = Gacha.objects.filter(cards__id=self.id)[0]
        except IndexError:
            gacha = None
        if gacha:
            self._cache_gacha_id = gacha.id
            self._cache_gacha_name = gacha.name
            self._cache_gacha_japanese_name = gacha.japanese_name
            self._cache_gacha_image = gacha.image
        else:
            self._cache_gacha_id = None

    def force_cache_gacha(self):
        self.update_cache_gacha()
        self.save()

    @property
    def cached_gacha(self):
        if not self._cache_gacha_last_update or self._cache_gacha_last_update < timezone.now() - datetime.timedelta(days=self._cache_gacha_days):
            self.force_cache_gacha()
        if not self._cache_gacha_id:
            return None
        return AttrDict({
            'pk': self._cache_gacha_id,
            'id': self._cache_gacha_id,
            'unicode': self._cache_gacha_name if get_language() != 'ja' else self._cache_gacha_japanese_name,
            'name': self._cache_gacha_name,
            'japanese_name': self._cache_gacha_japanese_name,
            'image': self._cache_gacha_image,
            'image_url': get_image_url_from_path(self._cache_gacha_image),
            'http_image_url': get_http_image_url_from_path(self._cache_gacha_image),
            'item_url': u'/gacha/{}/{}/'.format(self._cache_gacha_id, tourldash(self._cache_gacha_name)),
            'ajax_item_url': u'/ajax/gacha/{}/'.format(self._cache_gacha_id),
        })

    def __unicode__(self):
        if self.id:
            return u'{rarity} {member_name} - {attribute}'.format(
                rarity=self.rarity,
                member_name=(self.cached_member.japanese_name if get_language() == 'ja' else self.cached_member.name) if self.member_id else '',
                attribute=self.attribute,
            )
        return u''

############################################################
# Events

class Event(ItemModel):
    collection_name = 'event'

    owner = models.ForeignKey(User, related_name='added_events')
    image = models.ImageField(_('Image'), upload_to=uploadItem('e'))
    name = models.CharField(_('Title'), max_length=100, unique=True)
    japanese_name = models.CharField(string_concat(_('Title'), ' (', t['Japanese'], ')'), max_length=100, unique=True)
    start_date = models.DateTimeField(_('Beginning'), null=True)
    end_date = models.DateTimeField(_('End'), null=True)
    rare_stamp = models.ImageField(_('Rare Stamp'), upload_to=uploadItem('e/stamps'))
    @property
    def rare_stamp_url(self): return get_image_url_from_path(self.rare_stamp)
    @property
    def http_rare_stamp_url(self): return get_http_image_url_from_path(self.rare_stamp)

    stamp_translation = models.CharField(_('Stamp Translation'), max_length=200, null=True)

    main_card = models.ForeignKey(Card, related_name='main_card_event', null=True, limit_choices_to={
        'i_rarity': 3,
    }, on_delete=models.SET_NULL)
    secondary_card = models.ForeignKey(Card, related_name='secondary_card_event', null=True, limit_choices_to={
        'i_rarity': 2,
    }, on_delete=models.SET_NULL)

    i_boost_attribute = models.PositiveIntegerField(_('Boost Attribute'), choices=ATTRIBUTE_CHOICES, null=True)
    @property
    def boost_attribute(self): return ATTRIBUTE_DICT[self.i_boost_attribute] if self.i_boost_attribute else None
    @property
    def english_boost_attribute(self): return ENGLISH_ATTRIBUTE_DICT[self.i_boost_attribute] if self.i_boost_attribute else None

    boost_members = models.ManyToManyField(Member, related_name='boost_in_events', verbose_name=_('Boost Members'))

    @property
    def cached_gacha(self):
        # No need for a cache because the gacha is select_related in item view
        self.gacha.unicode = unicode(self.gacha)
        return self.gacha

    @property
    def status(self):
        if not self.end_date or not self.start_date:
            return None
        now = timezone.now()
        if now > self.end_date:
            return 'ended'
        elif now > self.start_date:
            return 'current'
        return 'future'

    def __unicode__(self):
        return unicode(self.japanese_name if get_language() == 'ja' and self.japanese_name else self.name)

############################################################
# Song

class Song(ItemModel):
    collection_name = 'song'

    DIFFICULTY_VALIDATORS = [
        MinValueValidator(1),
        MaxValueValidator(26),
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
    image = models.ImageField(_('Album cover'), upload_to=uploadItem('s'))

    i_band = models.PositiveIntegerField(_('Band'), choices=BAND_CHOICES)
    @property
    def band(self): return BAND_DICT[self.i_band]

    japanese_name = models.CharField(_('Title'), max_length=100, unique=True)
    romaji_name = models.CharField(string_concat(_('Title'), ' (', _('Romaji'), ')'), max_length=100, null=True)
    name = models.CharField(string_concat(_('Translation'), ' (', t['English'], ')'), max_length=100, null=True)

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

    i_unlock = models.PositiveIntegerField(_('How to unlock?'), choices=UNLOCK_CHOICES)
    @property
    def unlock(self): return UNLOCK_DICT.get(self.i_unlock, None)
    c_unlock_variables = models.CharField(max_length=100, null=True)
    @property
    def unlock_variables(self):
        return split_data(self.c_unlock_variables)
    @property
    def dict_unlock_variables(self):
        return {
            v: self.unlock_variables[i]
            for i, v in enumerate(UNLOCK_VARIABLES[self.unlock])
        }
    @property
    def unlock_sentence(self):
        return unicode(UNLOCK_SENTENCES[self.unlock]).format(**self.dict_unlock_variables)

    @property # Needed to use with types in magicollections
    def type(self):
        return self.unlock

    def __unicode__(self):
        return self.romaji_name if self.romaji_name and get_language() != 'ja'  else self.japanese_name

############################################################
# Gacha

class Gacha(ItemModel):
    collection_name = 'gacha'

    owner = models.ForeignKey(User, related_name='added_gacha')
    image = models.ImageField(_('Image'), upload_to=uploadItem('g'))
    name = models.CharField(_('Name'), max_length=100, unique=True)
    japanese_name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100, unique=True)
    start_date = models.DateTimeField(_('Beginning'), null=True)
    end_date = models.DateTimeField(_('End'), null=True)

    i_attribute = models.PositiveIntegerField(_('Attribute'), choices=ATTRIBUTE_CHOICES)
    @property
    def attribute(self): return ATTRIBUTE_DICT[self.i_attribute]
    @property
    def english_attribute(self): return ENGLISH_ATTRIBUTE_DICT[self.i_attribute]

    event = models.ForeignKey(Event, verbose_name=_('Event'), related_name='gachas', null=True, on_delete=models.SET_NULL)
    cards = models.ManyToManyField(Card, verbose_name=('Cards'), related_name='gachas')

    @property
    def cached_event(self):
        # No need for a cache because the event is select_related in item view
        self.event.unicode = unicode(self.event)
        return self.event

    @property
    def status(self):
        if not self.end_date or not self.start_date:
            return None
        now = timezone.now()
        if now > self.end_date:
            return 'ended'
        elif now > self.start_date:
            return 'current'
        return 'future'

    def __unicode__(self):
        return unicode(self.japanese_name if get_language() == 'ja' and self.japanese_name else self.name)
