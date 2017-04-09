# -*- coding: utf-8 -*-
from __future__ import division
import datetime
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.utils import timezone
from django.db.models import Q
from django.db import models
from django.conf import settings as django_settings
from web.models import User, uploadItem
from web.item_model import ItemModel, get_image_url_from_path, get_http_image_url_from_path
from web.utils import AttrDict, tourldash
from bang.model_choices import *
from bang.django_translated import t

############################################################
# Account

class Account(ItemModel):
    collection_name = 'account'

    owner = models.ForeignKey(User, related_name='accounts')
    creation = models.DateTimeField(_('Join Date'), auto_now_add=True)
    start_date = models.DateField(_('Start Date'), null=True)
    level = models.PositiveIntegerField(_("Level"), null=True)

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
        return self.japanese_name if get_language() == 'ja' else self.name

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

    # Skill

    # Labels for skill_names not translated because staff-only, members page shows "Title"
    skill_name = models.CharField('Skill name', max_length=100, null=True)
    japanese_skill_name = models.CharField('Skill name (Japanese)', max_length=100, null=True)
    i_skill_type = models.PositiveIntegerField(_('Skill'), choices=SKILL_TYPE_CHOICES)
    @property
    def skill_type(self): return SKILL_TYPE_DICT[self.i_skill_type]
    @property
    def japanese_skill_type(self): return JAPANESE_SKILL_TYPE_DICT[self.i_skill_type]
    skill_details = models.CharField(_('Skill'), max_length=500, null=True)

    @property
    def skill(self):
        return self.skill_details or SKILL_TEMPLATES[self.i_skill_type].format(size=SKILL_SIZES[self.i_rarity][0], note_type=SKILL_SIZES[self.i_rarity][2])

    @property
    def japanese_skill(self):
        return JAPANESE_SKILL_TEMPLATES[self.i_skill_type].format(size=SKILL_SIZES[self.i_rarity][1], note_type=SKILL_SIZES[self.i_rarity][2])

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
            'item_url': u'/member/{}/{}/'.format(self.member_id, tourldash(self._cache_member_name)),
            'ajax_item_url': u'/ajax/member/{}/'.format(self.member_id),
        })

    def __unicode__(self):
        if self.id:
            return u'{rarity} {member_name} - {attribute}'.format(
                rarity=self.rarity,
                member_name=self.cached_member.japanese_name if get_language() == 'ja' else self.cached_member.name,
                attribute=self.attribute,
            )
        return u''
