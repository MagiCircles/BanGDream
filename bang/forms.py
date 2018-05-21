from __future__ import division
import datetime, os
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.db.models.fields import BLANK_CHOICE_DASH
from django import forms
from magi.item_model import i_choices
from magi.utils import join_data, shrinkImageFromData, randomString, tourldash, PastOnlyValidator, getAccountIdsFromSession
from magi.forms import MagiForm, AutoForm, HiddenModelChoiceField, MagiFiltersForm, MagiFilter, MultiImageField, AccountForm as _AccountForm
from magi.middleware.httpredirect import HttpRedirectException
from bang import settings
from bang.django_translated import t
from bang import models

############################################################
# Users

class FilterUsers(MagiFiltersForm):
    search_fields = ('username', )
    ordering_fields = (
        ('username', t['Username']),
        ('join_date', _('Join Date')),
    )

    favorited_card = forms.IntegerField(widget=forms.HiddenInput)
    favorited_card_filter = MagiFilter(selector='favorite_cards__card_id')

    class Meta(MagiFiltersForm.Meta):
        model = models.User
        fields = ('search', 'ordering', 'reverse_order')

############################################################
# Accounts

class AccountForm(_AccountForm):
    level = forms.IntegerField(required=False, label=_('Level'), validators=[
        MinValueValidator(1),
        MaxValueValidator(300),
    ])
    start_date = forms.DateField(required=False, label=_('Start Date'), validators=[
        PastOnlyValidator,
        MinValueValidator(datetime.date(2017, 3, 16)),
    ])

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        if 'center' in self.fields:
            self.fields['center'].queryset = self.fields['center'].queryset.select_related('card').order_by('-card__release_date', '-card__id')
        if 'stargems_bought' in self.fields:
            self.fields['stargems_bought'].label = _('Total {item} bought').format(item=_('Star gems').lower())

    def save(self, commit=False):
        instance = super(AccountForm, self).save(commit=False)
        if instance.stargems_bought == 0:
            instance.stargems_bought = None
        if commit:
            instance.save()
        return instance

class AddAccountForm(AccountForm):
    def __init__(self, *args, **kwargs):
        super(AddAccountForm, self).__init__(*args, **kwargs)
        if not self.data.get('screenshot') and 'screenshot' in self.fields and int(self.data.get('level', 0) or 0) < 200:
            self.fields['screenshot'].widget = forms.HiddenInput()
        if 'start_date' in self.fields:
            del(self.fields['start_date'])

    class Meta(AccountForm.Meta):
        fields = ('nickname', 'i_version', 'level', 'friend_id', 'screenshot')

class FilterAccounts(MagiFiltersForm):
    search_fields = ['owner__username', 'owner__preferences__description', 'owner__preferences__location', 'owner__links__value']
    search_fields_exact = ['owner__email']

    ordering_fields = [
        ('level', _('Level')),
        ('owner__username', t['Username']),
        ('creation', _('Join Date')),
        ('start_date', _('Start Date')),
    ]

    member = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])], required=False, label=_('Favorite Member'))
    member_filter = MagiFilter(selectors=['owner__preferences__favorite_character{}'.format(i) for i in range(1, 4)])

    has_friend_id = forms.NullBooleanField(required=False, initial=None, label=_('Friend ID'))
    has_friend_id_filter = MagiFilter(selector='friend_id__isnull')

    i_color = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(c[0], c[1]) for c in settings.USER_COLORS], required=False, label=_('Color'))
    i_color_filter = MagiFilter(selector='owner__preferences__color')

    collected_card = forms.IntegerField(widget=forms.HiddenInput)
    collected_card_filter = MagiFilter(selector='cardscollectors__card_id')

    class Meta(MagiFiltersForm.Meta):
        model = models.Account
        fields = ('search', 'friend_id', 'i_version', 'i_color', 'member', 'has_friend_id')

############################################################
# Member

class MemberForm(AutoForm):
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        # Change labels for staff
        self.fields['square_image'].label = 'Small icon (for the map)'
        self.fields['square_image'].help_text = mark_safe('Example: <img src="https://i.bandori.party/u/i/m/1Toyama-Kasumi-D7Fpvu.png" height="40">')

    def save(self, commit=False):
        instance = super(MemberForm, self).save(commit=False)
        # Invalidate cards cache
        if not self.is_creating:
            models.Card.objects.filter(member_id=instance.id).update(_cache_member_last_update=None)
        if commit:
            instance.save()
        return instance

    class Meta(AutoForm.Meta):
        model = models.Member
        fields = '__all__'
        save_owner_on_creation = True

class MemberFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name', 'school', 'CV', 'romaji_CV', 'food_like', 'food_dislike', 'instrument', 'hobbies', 'description']

    ordering_fields = [
        ('id', _('Band')),
        ('_cache_total_fans', _('Popularity')),
        ('name', _('Name')),
        ('japanese_name', string_concat(_('Name'), ' (', t['Japanese'], ')')),
        ('birthday', _('Birthday')),
    ]

    school = forms.ChoiceField(label=_('School'), choices=BLANK_CHOICE_DASH + [(s, s) for s in getattr(django_settings, 'SCHOOLS', [])], initial=None)

    class Meta(MagiFiltersForm.Meta):
        model = models.Member
        fields = ('search', 'i_band', 'school', 'i_school_year', 'i_astrological_sign')

############################################################
# Card

class CardForm(AutoForm):
    chibis = MultiImageField(min_num=0, max_num=10, required=False, label='Add chibi images')

    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        self.previous_member_id = None if self.is_creating else self.instance.member_id
        # Delete existing chibis
        if not self.is_creating:
            self.all_chibis = self.instance.chibis.all()
            for imageObject in self.all_chibis:
                self.fields[u'delete_chibi_{}'.format(imageObject.id)] = forms.BooleanField(
                    label=mark_safe(u'Delete chibi <img src="{}" height="100" />'.format(imageObject.image_url)),
                    initial=False, required=False,
                )

    def save(self, commit=False):
        instance = super(CardForm, self).save(commit=False)
        if self.previous_member_id != instance.member_id:
            instance.update_cache('member')
        instance.save()
        # Delete existing chibis
        if not self.is_creating:
            for imageObject in self.all_chibis:
                field_name = u'delete_chibi_{}'.format(imageObject.id)
                field = self.fields.get(field_name)
                if field and self.cleaned_data[field_name]:
                    instance.chibis.remove(imageObject)
                    imageObject.delete()
        # Upload new chibis
        for image in self.cleaned_data['chibis']:
            if isinstance(image, int):
                continue
            name, extension = os.path.splitext(image.name)
            imageObject = models.Image.objects.create()
            image = shrinkImageFromData(image.read(), image.name)
            image.name = u'{name}-{attribute}-chibi.{extension}'.format(
                name=tourldash(instance.member.name),
                attribute=instance.english_attribute,
                extension=extension,
            )
            imageObject.image.save(image.name, image)
            instance.chibis.add(imageObject)
        instance.force_cache_chibis()
        # members can't cameo in their own cards
        instance.cameo_members = filter(lambda x: x.id != instance.member_id, self.cleaned_data['cameo_members'])
        instance.update_cache('cameos')
        return instance

    class Meta(AutoForm.Meta):
        model = models.Card
        fields = '__all__'
        optional_fields = ('cameo_members',)
        save_owner_on_creation = True

def to_translate_card_form_class(cls):
    class _TranslateCardForm(cls):
        class Meta(cls.Meta):
            fields = ['name', 'japanese_name', 'skill_name', 'japanese_skill_name'] + cls.Meta.fields
    return _TranslateCardForm

class CardFilterForm(MagiFiltersForm):
    search_fields = ['_cache_j_member', 'name', 'japanese_name', 'skill_name', 'japanese_skill_name']
    ordering_fields = [
        ('release_date,id', _('Release date')),
        ('id', _('ID')),
        ('_cache_total_collectedcards', lambda: string_concat(_('Popularity'), ' (', _('Collected {things}').format(things=_('Cards').lower()), ')')),
        ('_cache_total_favorited', lambda: string_concat(_('Popularity'), ' (', _('Favorite {things}').format(things=_('Cards').lower()), ')')),
        ('member__name', string_concat(_('Member'), ' - ', _('Name'))),
        ('member__japanese_name', string_concat(_('Member'), ' - ', _('Name'), ' (', t['Japanese'], ')')),
        ('i_rarity', _('Rarity')),
        ('i_attribute', _('Attribute')),
        ('performance_max', _('Performance')),
        ('performance_trained_max', string_concat(_('Performance'), ' (', _('Trained'), ')')),
        ('technique_max', _('Technique')),
        ('technique_trained_max', string_concat(_('Technique'), ' (', _('Trained'), ')')),
        ('visual_max', _('Visual')),
        ('visual_trained_max', string_concat(_('Visual'), ' (', _('Trained'), ')')),
        ('_overall_max', _('Overall')),
        ('_overall_trained_max', string_concat(_('Overall'), ' (', _('Trained'), ')')),
    ]

    def skill_filter_to_queryset(self, queryset, request, value):
        if not value: return queryset
        if value == '1': return queryset.filter(i_skill_type=value) # Score up
        return queryset.filter(Q(i_skill_type=value) | Q(i_side_skill_type=value))
    i_skill_type_filter = MagiFilter(to_queryset=skill_filter_to_queryset)

    def member_id_to_queryset(self, queryset, request, value):
        if self.data.get('member_includes_cameos'):
            return queryset.filter(Q(member_id=value) | Q(cameo_members__id=value))
        else:
            return queryset.filter(member_id=value)

    member = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])], initial=None, label=_('Member'))

    member_includes_cameos = forms.BooleanField(label=_('Include cameos'))
    # used in member_id_to_queryset
    member_includes_cameos_filter = MagiFilter(noop=True)

    member_band = forms.ChoiceField(choices=BLANK_CHOICE_DASH + i_choices(models.Member.BAND_CHOICES), initial=None, label=_('Band'))
    member_band_filter = MagiFilter(selector='member__i_band')

    def _origin_to_queryset(self, queryset, request, value):
        if value == 'is_original':
            return queryset.filter(is_original=True)
        elif value == 'is_promo':
            return queryset.filter(is_promo=True)
        elif value == 'is_gacha':
            return queryset.filter(_cache_j_gachas__isnull=False)
        elif value == 'is_event':
            return queryset.filter(_cache_j_events__isnull=False)
        return queryset

    origin = forms.ChoiceField(label=_(u'Origin'), choices=BLANK_CHOICE_DASH + [
        ('is_original', _(u'Original')),
        ('is_event', _(u'Event')),
        ('is_gacha', _(u'Gacha')),
        ('is_promo', _(u'Promo')),
    ])
    origin_filter = MagiFilter(to_queryset=_origin_to_queryset)

    is_limited = forms.NullBooleanField(initial=None, required=False, label=_('Limited'))
    is_limited_filter = MagiFilter(selector='gachas__limited')

    def _view_to_queryset(self, queryset, request, value):
        if value == 'chibis':
            return queryset.filter(_cache_chibis_ids__isnull=False).exclude(_cache_chibis_ids='')
        elif value == 'live2d':
            return queryset.filter(live2d_model_pkg__isnull=False).exclude(live2d_model_pkg='')
        elif value == 'art':
            return queryset.filter(art__isnull=False)
        elif value == 'transparent':
            return queryset.filter(transparent__isnull=False)
        return queryset

    view_filter = MagiFilter(to_queryset=_view_to_queryset)

    version = forms.ChoiceField(label=_(u'Server availability'), choices=BLANK_CHOICE_DASH + models.Account.VERSION_CHOICES)
    version_filter = MagiFilter(to_queryset=lambda form, queryset, request, value: queryset.filter(c_versions__contains=value))

    class Meta(MagiFiltersForm.Meta):
        model = models.Card
        fields = ('view', 'search', 'member', 'member_includes_cameos', 'member_band', 'i_rarity', 'i_attribute', 'origin', 'is_limited', 'i_skill_type', 'member_band', 'version', 'ordering', 'reverse_order')

############################################################
# CollectibleCard

def to_CollectibleCardForm(cls):
    class _CollectibleCardForm(cls.form_class):
        def __init__(self, *args, **kwargs):
            super(_CollectibleCardForm, self).__init__(*args, **kwargs)
            if 'first_episode' in self.fields:
                self.fields['first_episode'].label = _('{nth} episode').format(nth=_('1st'))
            rarity = int(self.collectible_variables['i_rarity'])
            if rarity and rarity not in models.Card.TRAINABLE_RARITIES and 'trained' in self.fields:
                del(self.fields['trained'])
                if 'prefer_untrained' in self.fields:
                    del(self.fields['prefer_untrained'])

        def save(self, commit=True):
            instance = super(_CollectibleCardForm, self).save(commit=False)
            if instance.card.i_rarity not in models.Card.TRAINABLE_RARITIES:
                instance.trained = False
            if commit:
                instance.save()
            return instance
    return _CollectibleCardForm

def to_CollectibleCardFilterForm(cls):
    class _CollectibleCardFilterForm(cls.ListView.filter_form):
        search_fields = [u'card__{}'.format(_o) for _o in CardFilterForm.search_fields]
        ordering_fields = [(u'card__{}'.format(_o), _t) for _o, _t in CardFilterForm.ordering_fields]
        def skill_filter_to_queryset(self, queryset, request, value):
            if not value: return queryset
            if value == '1': return queryset.filter(card__i_skill_type=value) # Score up
            return queryset.filter(Q(card__i_skill_type=value) | Q(card__i_side_skill_type=value))

        member = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])], initial=None, label=_('Member'))
        member_filter = MagiFilter(selector='card__member_id')

        member_band = forms.ChoiceField(choices=BLANK_CHOICE_DASH + i_choices(models.Member.BAND_CHOICES), initial=None, label=_('Band'))
        member_band_filter = MagiFilter(selector='card__member__i_band')

        i_rarity = forms.ChoiceField(choices=BLANK_CHOICE_DASH + list(models.Card.RARITY_CHOICES), label=_('Rarity'))
        i_rarity_filter = MagiFilter(selector='card__i_rarity')

        i_attribute = forms.ChoiceField(choices=BLANK_CHOICE_DASH + list(models.Card.ATTRIBUTE_CHOICES), label=_('Attribute'))
        i_attribute_filter = MagiFilter(selector='card__i_attribute')

        i_skill_type = forms.ChoiceField(choices=BLANK_CHOICE_DASH
                                               + models.Card.SKILL_TYPE_CHOICES, label=_('Skill'))
        i_skill_type_filter = MagiFilter(to_queryset=skill_filter_to_queryset)

        class Meta(cls.ListView.filter_form.Meta):
            pass
            fields = ('search', 'member', 'member_band', 'i_rarity', 'i_attribute', 'i_skill_type', 'member_band', 'ordering', 'reverse_order', 'view')
    return _CollectibleCardFilterForm

############################################################
# Event

class EventForm(AutoForm):
    start_date = forms.DateField(label=_('Beginning'))
    end_date = forms.DateField(label=_('End'))

    english_start_date = forms.DateField(label=string_concat(_('English version'), ' - ', _('Beginning')), required=False)
    english_end_date = forms.DateField(label=string_concat(_('English version'), ' - ', _('End')), required=False)

    taiwanese_start_date = forms.DateField(label=string_concat(_('Taiwanese version'), ' - ', _('Beginning')), required=False)
    taiwanese_end_date = forms.DateField(label=string_concat(_('Taiwanese version'), ' - ', _('End')), required=False)

    korean_start_date = forms.DateField(label=string_concat(_('Korean version'), ' - ', _('Beginning')), required=False)
    korean_end_date = forms.DateField(label=string_concat(_('Korean version'), ' - ', _('End')), required=False)

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if not self.is_creating:
            self.instance.previous_main_card_id = self.instance.main_card_id
            self.instance.previous_secondary_card_id = self.instance.secondary_card_id

        # Exclude invalid cards
        for prefix in ['main', 'secondary']:
            try:
                queryset = self.fields['{}_card'.format(prefix)].queryset.filter(
                    gachas__isnull=True,
                    is_promo=False,
                    is_original=False,
                )
            except KeyError:
                continue
            if not self.is_creating:
                queryset = queryset.filter(
                    Q(main_card_event__isnull=True, secondary_card_event__isnull=True)
                    | Q(**{ '{}_card_event__id'.format(prefix): self.instance.id }),
                )
            else:
                queryset = queryset.filter(main_card_event__isnull=True, secondary_card_event__isnull=True)
            self.fields['{}_card'.format(prefix)].queryset = queryset

        if 'c_versions' in self.fields:
            del(self.fields['c_versions'])

    def _clean_card_rarity(self, field_name, rarities):
        if field_name in self.cleaned_data and self.cleaned_data[field_name]:
            if self.cleaned_data[field_name].i_rarity not in rarities:
                raise forms.ValidationError(u'Rarity must be one of {}'.format(tuple(rarities)))
            return self.cleaned_data[field_name]
        return None

    def clean_main_card(self):
        return self._clean_card_rarity('main_card', models.Event.MAIN_CARD_ALLOWED_RARITIES)

    def clean_secondary_card(self):
        return self._clean_card_rarity('secondary_card', models.Event.SECONDARY_CARD_ALLOWED_RARITIES)

    def save(self, commit=False):
        instance = super(EventForm, self).save(commit=False)
        if instance.start_date:
            instance.start_date = instance.start_date.replace(hour=6, minute=00)
        if instance.end_date:
            instance.end_date = instance.end_date.replace(hour=11, minute=59)
        if instance.english_start_date:
            instance.english_start_date = instance.english_start_date.replace(hour=1, minute=00)
        if instance.english_end_date:
            instance.english_end_date = instance.english_end_date.replace(hour=6, minute=59)
        if instance.taiwanese_start_date:
            instance.taiwanese_start_date = instance.taiwanese_start_date.replace(hour=7, minute=00)
        if instance.taiwanese_end_date:
            instance.taiwanese_end_date = instance.taiwanese_end_date.replace(hour=13, minute=59)
        if instance.korean_start_date:
            instance.korean_start_date = instance.korean_start_date.replace(hour=6, minute=00)
        if instance.korean_end_date:
            instance.korean_end_date = instance.korean_end_date.replace(hour=13, minute=00)
        instance.save_c('versions', [
            value for prefix, value in (
                ('', 'JP'),
                ('english_', 'EN'),
                ('taiwanese_', 'TW'),
                ('korean_', 'KR'),
            ) if getattr(instance, u'{}start_date'.format(prefix))])
        if commit:
            instance.save()
        return instance

    class Meta(AutoForm.Meta):
        model = models.Event
        fields = '__all__'
        optional_fields = ('boost_members',)
        save_owner_on_creation = True

def to_translate_event_form_class(cls):
    class _TranslateEventForm(cls):
        class Meta(cls.Meta):
            fields = ['name', 'japanese_name'] + cls.Meta.fields
    return _TranslateEventForm

class EventFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name']
    ordering_fields = [
        ('start_date', string_concat(_('Date'), ' (', _('Japanese version'), ')')),
        ('english_start_date', string_concat(_('Date'), ' (', _('English version'), ')')),
        ('taiwanese_start_date', string_concat(_('Date'), ' (', _('Taiwanese version'), ')')),
        ('korean_start_date', string_concat(_('Date'), ' (', _('Korean version'), ')')),
        ('_cache_total_participations', string_concat(_('Popularity'), ' (', _('Participated events'), ')')),
        ('name', _('Title')),
        ('japanese_name', string_concat(_('Title'), ' (', t['Japanese'], ')')),
    ]

    boost_members = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])], initial=None, label=_('Boost members'))

    version = forms.ChoiceField(label=_(u'Server availability'), choices=BLANK_CHOICE_DASH + models.Account.VERSION_CHOICES)
    version_filter = MagiFilter(to_queryset=lambda form, queryset, request, value: queryset.filter(c_versions__contains=value))

    class Meta(MagiFiltersForm.Meta):
        model = models.Event
        fields = ('view', 'search', 'i_type', 'boost_members', 'i_boost_attribute', 'version', 'ordering', 'reverse_order')

############################################################
# Event participations form

def to_EventParticipationForm(cls):
    class _EventParticipationForm(cls.form_class):
        def __init__(self, *args, **kwargs):
            super(_EventParticipationForm, self).__init__(*args, **kwargs)
            i_type = int(self.collectible_variables['i_type'])
            if models.Event.get_reverse_i('type', i_type) not in models.Event.SONG_RANKING_TYPES:
                for field in ['song_score', 'song_ranking']:
                    if field in self.fields:
                        del(self.fields[field])
            if models.Event.get_reverse_i('type', i_type) not in models.Event.TRIAL_MASTER_TYPES:
                for field in ['is_trial_master_completed', 'is_trial_master_ex_completed']:
                    if field in self.fields:
                        del(self.fields[field])

        class Meta(cls.form_class.Meta):
            optional_fields = ('score', 'ranking', 'song_score', 'song_ranking')

    return _EventParticipationForm

def to_EventParticipationFilterForm(cls):
    class _EventParticipationFilterForm(cls.ListView.filter_form):
        search_fields = [u'event__{}'.format(_o) for _o in EventFilterForm.search_fields]
        ordering_fields = [
            ('id', _('Creation')),
            ('ranking', _('Ranking')),
            ('score', _('Score')),
            ('song_score', _('Song score')),
            ('song_ranking', _('Song ranking')),
        ] + [(u'event__{}'.format(_o), _t) for _o, _t in EventFilterForm.ordering_fields]

        i_version = forms.ChoiceField(label=_('Version'), choices=BLANK_CHOICE_DASH + i_choices(models.Account.VERSION_CHOICES))
        i_version_filter = MagiFilter(selector='account__i_version')

        # TODO: event type, boost members, boost attribute

        def __init__(self, *args, **kwargs):
            super(_EventParticipationFilterForm, self).__init__(*args, **kwargs)
            if 'view' in self.fields and self.request.GET.get('view', None) != 'leaderboard':
                del(self.fields['view'])

        class Meta(cls.ListView.filter_form.Meta):
            fields = ('view', 'search', 'i_version', 'ordering', 'reverse_order')

    return _EventParticipationFilterForm

############################################################
# Gacha

class GachaForm(AutoForm):
    start_date = forms.DateField(label=_('Beginning'))
    end_date = forms.DateField(label=_('End'))

    english_start_date = forms.DateField(label=string_concat(_('English version'), ' - ', _('Beginning')), required=False)
    english_end_date = forms.DateField(label=string_concat(_('English version'), ' - ', _('End')), required=False)

    taiwanese_start_date = forms.DateField(label=string_concat(_('Taiwanese version'), ' - ', _('Beginning')), required=False)
    taiwanese_end_date = forms.DateField(label=string_concat(_('Taiwanese version'), ' - ', _('End')), required=False)

    korean_start_date = forms.DateField(label=string_concat(_('Korean version'), ' - ', _('Beginning')), required=False)
    korean_end_date = forms.DateField(label=string_concat(_('Korean version'), ' - ', _('End')), required=False)

    def __init__(self, *args, **kwargs):
        super(GachaForm, self).__init__(*args, **kwargs)

        # Exclude invalid cards
        if 'cards' in self.fields:
            queryset = self.fields['cards'].queryset.filter(
                main_card_event__isnull=True,
                secondary_card_event__isnull=True,
                is_promo=False,
                is_original=False,
            )
            if self.is_creating:
                queryset = queryset.filter(gachas__isnull=True)
            elif not self.instance.dreamfes:
                queryset = queryset.filter(Q(gachas__isnull=True) | Q(gachas__id=self.instance.id))
            self.fields['cards'].queryset = queryset

        if 'c_versions' in self.fields:
            del(self.fields['c_versions'])

    def save(self, commit=False):
        instance = super(GachaForm, self).save(commit=False)
        if instance.start_date:
            instance.start_date = instance.start_date.replace(hour=6, minute=00)
        if instance.end_date:
            instance.end_date = instance.end_date.replace(hour=5, minute=59)
        if instance.english_start_date:
            instance.english_start_date = instance.english_start_date.replace(hour=1, minute=00)
        if instance.english_end_date:
            instance.english_end_date = instance.english_end_date.replace(hour=0, minute=59)
        if instance.taiwanese_start_date:
            instance.taiwanese_start_date = instance.taiwanese_start_date.replace(hour=7, minute=00)
        if instance.taiwanese_end_date:
            instance.taiwanese_end_date = instance.taiwanese_end_date.replace(hour=6, minute=59)
        if instance.korean_start_date:
            instance.korean_start_date = instance.korean_start_date.replace(hour=6, minute=00)
        if instance.korean_end_date:
            instance.korean_end_date = instance.korean_end_date.replace(hour=6, minute=00)
        instance.save_c('versions', [
            value for prefix, value in (
                ('', 'JP'),
                ('english_', 'EN'),
                ('taiwanese_', 'TW'),
                ('korean_', 'KR'),
            ) if getattr(instance, u'{}start_date'.format(prefix))])
        if commit:
            instance.save()
        return instance

    class Meta(AutoForm.Meta):
        model = models.Gacha
        fields = '__all__'
        optional_fields = ('cards',)
        save_owner_on_creation = True

def to_translate_gacha_form_class(cls):
    class _TranslateGachaForm(cls):
        class Meta(cls.Meta):
            fields = ['name', 'japanese_name'] + cls.Meta.fields
    return _TranslateGachaForm

class GachaFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name']
    ordering_fields = [
        ('start_date', string_concat(_('Date'), ' (', _('Japanese version'), ')')),
        ('english_start_date', string_concat(_('Date'), ' (', _('English version'), ')')),
        ('taiwanese_start_date', string_concat(_('Date'), ' (', _('Taiwanese version'), ')')),
        ('korean_start_date', string_concat(_('Date'), ' (', _('Korean version'), ')')),
        ('name', _('Title')),
        ('japanese_name', string_concat(_('Title'), ' (', t['Japanese'], ')')),
    ]

    def _gacha_type_to_queryset(self, queryset, request, value):
        if value == 'permanent':
            return queryset.filter(limited=False, dreamfes=False)
        elif value == 'limited':
            return queryset.filter(limited=True)
        elif value == 'dreamfes':
            return queryset.filter(dreamfes=True)
        return queryset

    gacha_type = forms.ChoiceField(label=_(u'Gacha type'), choices=BLANK_CHOICE_DASH + [
        ('permanent', _(u'Permanent')),
        ('limited', _(u'Limited')),
        ('dreamfes', 'Dream festival'),
    ])
    gacha_type_filter = MagiFilter(to_queryset=_gacha_type_to_queryset)

    featured_member = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])], initial=None, label=_('Member'))
    featured_member_filter = MagiFilter(selector='cards__member_id')

    version = forms.ChoiceField(label=_(u'Server availability'), choices=BLANK_CHOICE_DASH + models.Account.VERSION_CHOICES)
    version_filter = MagiFilter(to_queryset=lambda form, queryset, request, value: queryset.filter(c_versions__contains=value))

    def __init__(self, *args, **kwargs):
        super(GachaFilterForm, self).__init__(*args, **kwargs)
        if 'gacha_type' in self.fields:
            self.fields['gacha_type'].choices = [
                (k, models.DREAMFES_PER_LANGUAGE.get(get_language(), v) if k == 'dreamfes' else v)
                for k, v in self.fields['gacha_type'].choices
            ]

    class Meta(MagiFiltersForm.Meta):
        model = models.Gacha
        fields = ('search', 'gacha_type', 'featured_member', 'i_attribute', 'version', 'ordering', 'reverse_order')

############################################################
# Played song

def to_PlayedSongForm(cls):
    class _PlayedSongForm(cls.form_class):
        class Meta(cls.form_class.Meta):
            optional_fields = ('score', 'screenshot')
    return _PlayedSongForm

def to_PlayedSongFilterForm(cls):
    class _PlayedSongFilterForm(cls.ListView.filter_form):
        search_fields = [u'song__{}'.format(_o) for _o in SongFilterForm.search_fields]
        ordering_fields = [
            ('id', _('Creation')),
            ('score', _('Score')),
        ] + [(u'song__{}'.format(_o), _t) for _o, _t in SongFilterForm.ordering_fields]

        i_version = forms.ChoiceField(label=_('Version'), choices=BLANK_CHOICE_DASH + i_choices(models.Account.VERSION_CHOICES))
        i_version_filter = MagiFilter(selector='account__i_version')

        screenshot = forms.NullBooleanField(label=_('Screenshot'))
        screenshot_filter = MagiFilter(selector='screenshot__isnull')

        # TODO: band, unlock, cover

        def __init__(self, *args, **kwargs):
            super(_PlayedSongFilterForm, self).__init__(*args, **kwargs)
            if 'view' in self.fields and self.request.GET.get('view', None) != 'leaderboard':
                self.fields['view'].choices = [(k, v) for k, v in self.fields['view'].choices if k != 'leaderboard']

        class Meta(cls.ListView.filter_form.Meta):
            fields = ('view', 'search', 'i_version', 'i_difficulty', 'full_combo', 'all_perfect', 'screenshot', 'ordering', 'reverse_order')

    return _PlayedSongFilterForm

############################################################
# Song

class _SongForm(AutoForm):

    def __init__(self, *args, **kwargs):
        super(_SongForm, self).__init__(*args, **kwargs)
        if 'i_unlock' in self.fields:
            del(self.fields['i_unlock'])
        if 'c_unlock_variables' in self.fields:
            del(self.fields['c_unlock_variables'])
        if 'length' in self.fields:
            self.fields['length'].help_text = 'in seconds'

    class Meta(AutoForm.Meta):
        model = models.Song
        fields = '__all__'
        save_owner_on_creation = True

def unlock_to_form(unlock):
    class _UnlockSongForm(_SongForm):
        def __init__(self, *args, **kwargs):
            super(_UnlockSongForm, self).__init__(*args, **kwargs)
            help_text = mark_safe(u'Will be displayed as <code>{}</code>'.format(
                unicode(models.Song.UNLOCK[unlock]['template']).format(**{
                    variable: 'xxx'
                    for variable in models.Song.UNLOCK[unlock]['variables']
                }),
            )) if unlock != 'other' else None
            for i, variable in enumerate(models.Song.UNLOCK[unlock]['variables']):
                self.fields[variable] = forms.CharField(
                    help_text=help_text,
                    initial=None if self.is_creating else self.instance.unlock_variables[i],
                )
            if unlock != 'event' and 'event' in self.fields:
                del(self.fields['event'])

        def save(self, commit=False):
            instance = super(_UnlockSongForm, self).save(commit=False)
            instance.i_unlock = models.Song.get_i('unlock', unlock)
            instance.c_unlock_variables = join_data(*[
                self.cleaned_data[variable]
                for variable in models.Song.UNLOCK[unlock]['variables']
            ])
            if commit:
                instance.save()
            return instance

    return _UnlockSongForm

def to_translate_song_form_class(cls):
    class _TranslateSongForm(cls):
        class Meta(cls.Meta):
            fields = ['name', 'japanese_name', 'romaji_name'] + cls.Meta.fields
    return _TranslateSongForm

class SongFilterForm(MagiFiltersForm):
    search_fields = ['japanese_name', 'romaji_name', 'name', 'composer', 'lyricist', 'arranger', 'c_unlock_variables']
    ordering_fields = [
        ('release_date', _('Release date')),
        ('japanese_name', _('Title')),
        ('_cache_total_played', string_concat(_('Popularity'), ' (', _('Played songs'), ')')),
        ('romaji_name', string_concat(_('Title'), ' (', _('Romaji'), ')')),
        ('length', _('Length')),
        ('bpm', _('BPM')),
        ('hard_notes', string_concat(_('Hard'), ' - ', _('Notes'))),
        ('hard_difficulty', string_concat(_('Hard'), ' - ', _('Difficulty'))),
        ('expert_notes', string_concat(_('Expert'), ' - ', _('Notes'))),
        ('expert_difficulty', string_concat(_('Expert'), ' - ', _('Difficulty'))),
    ]

    is_cover = forms.NullBooleanField(initial=None, required=False, label=_('Cover'))
    is_cover_filter = MagiFilter(selector='is_cover')

    version = forms.ChoiceField(label=_(u'Server availability'), choices=BLANK_CHOICE_DASH + models.Account.VERSION_CHOICES)
    version_filter = MagiFilter(to_queryset=lambda form, queryset, request, value: queryset.filter(c_versions__contains=value))

    class Meta(MagiFiltersForm.Meta):
        model = models.Song
        fields = ('search', 'i_band', 'i_unlock', 'is_cover', 'version', 'ordering', 'reverse_order')

############################################################
# Area form

class AreaForm(AutoForm):
    class Meta(AutoForm.Meta):
        model = models.Area
        fields = '__all__'
        save_owner_on_creation = True

############################################################
# Area item form

def areaitem_type_to_form(type):
    class _AreaItemForm(AutoForm):
        def __init__(self, *args, **kwargs):
            super(_AreaItemForm, self).__init__(*args, **kwargs)
            for variable in models.AreaItem.VARIABLES:
                if variable in self.fields and variable not in models.AreaItem.TYPES[type]['variables']:
                    del(self.fields[variable])
            if 'i_type' in self.fields:
                del(self.fields['i_type'])

        def save(self, commit=False):
            instance = super(_AreaItemForm, self).save(commit=False)
            instance.i_type = models.AreaItem.get_i('type', type)
            if instance.member_id:
                instance.i_band = instance.member.i_band
            if commit:
                instance.save()
            return instance

        class Meta(AutoForm.Meta):
            model = models.AreaItem
            fields = '__all__'
            save_owner_on_creation = True
    return _AreaItemForm

class AreaItemFilters(MagiFiltersForm):
    search_fields = ['area__name', 'area__d_names', 'name', 'd_names', 'instrument', 'd_instruments']

    i_type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [('instrument', _('Instrument'))] + [
        (i, d['translation']) for i, (k, d) in enumerate(models.AreaItem.TYPES.items())
        if not k.startswith('instrument_')
    ], label=_('Type'))
    i_type_filter = MagiFilter(to_queryset=lambda form, queryset, request, value: queryset.filter(i_type__in=[
        models.AreaItem.get_i('type', 'instrument_per_member'),
        models.AreaItem.get_i('type', 'instrument_per_band'),
    ]) if value == 'instrument' else queryset.filter(i_type=value))

    member = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])], initial=None, label=_('Member'))

    area = forms.IntegerField(widget=forms.HiddenInput)

    class Meta(MagiFiltersForm.Meta):
        model = models.AreaItem
        fields = ('search', 'i_type', 'i_band', 'member', 'i_attribute', 'i_stat', 'area')

############################################################
# Item form

class ItemForm(AutoForm):
    class Meta(AutoForm.Meta):
        model = models.Item
        fields = '__all__'
        save_owner_on_creation = True

############################################################
# Item form

def to_CollectibleAreaItemForm(cls):
    class _CollectibleAreaItemForm(cls.form_class):
        level = forms.IntegerField(required=False, label=_('Level'), validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ])

        def __init__(self, *args, **kwargs):
            super(_CollectibleAreaItemForm, self).__init__(*args, **kwargs)
            _type = self.collectible_variables.get('type')
            if _type and _type == 'instrument_per_band' and 'level' in self.fields:
                self.fields['level'].validators = [
                    MinValueValidator(1),
                    MaxValueValidator(6),
                ]

    return _CollectibleAreaItemForm

############################################################
# Asset form

class AssetForm(AutoForm):
    class Meta(AutoForm.Meta):
        model = models.Asset
        fields = '__all__'
        save_owner_on_creation = True

def asset_type_to_form(_type):
    class _AssetForm(AutoForm):
        def __init__(self, *args, **kwargs):
            super(_AssetForm, self).__init__(*args, **kwargs)
            for variable in models.Asset.VARIABLES:
                if variable in self.fields and variable not in models.Asset.TYPES[_type]['variables']:
                    del(self.fields[variable])
            if 'i_type' in self.fields:
                del(self.fields['i_type'])

        def save(self, commit=False):
            instance = super(_AssetForm, self).save(commit=False)
            instance.i_type = models.Asset.get_i('type', _type)
            if not instance.c_tags:
                instance.c_tags = None
            if instance.member_id:
                instance.i_band = instance.member.i_band
            if commit:
                instance.save()
            return instance

        class Meta(AutoForm.Meta):
            model = models.Asset
            fields = '__all__'
            save_owner_on_creation = True
    return _AssetForm

class AssetFilterForm(MagiFiltersForm):
    search_fields = ('name', 'd_names', 'c_tags')

    member = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])], initial=None, label=_('Member'))

    def _i_version_to_queryset(self, queryset, request, value):
        prefix = models.Account.VERSIONS_PREFIXES.get(models.Account.get_reverse_i('version', int(value)))
        return queryset.filter(**{
            u'{}image__isnull'.format(prefix): False,
        }).exclude(**{
            u'{}image'.format(prefix): '',
        })

    i_version = forms.ChoiceField(label=_('Version'), choices=BLANK_CHOICE_DASH + i_choices(models.Account.VERSION_CHOICES))
    i_version_filter = MagiFilter(to_queryset=_i_version_to_queryset)

    event = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(AssetFilterForm, self).__init__(*args, **kwargs)
        try:
            type = models.Asset.get_reverse_i('type', int(self.request.GET.get('i_type', None)))
        except (KeyError, ValueError, TypeError):
            type = None
        if type in models.Asset.TYPES:
            for variable in models.Asset.VARIABLES:
                if (variable in self.fields
                    and variable not in (
                        models.Asset.TYPES[type]['variables']
                        + (['i_band'] if 'member' in models.Asset.TYPES[type]['variables'] else [])
                    )):
                    del(self.fields[variable])
            if 'i_type' in self.fields:
                self.fields['i_type'].widget = forms.HiddenInput()

    class Meta(MagiFiltersForm.Meta):
        model = models.Asset
        fields = ['search', 'i_type'] + [
            v for v in models.Asset.VARIABLES if v not in ['name', 'value']
        ] + ['i_version']

############################################################
# Costume form
class CostumeForm(AutoForm):
    def __init__(self, *args, **kwargs):
        super(CostumeForm, self).__init__(*args, **kwargs)
        if not self.is_creating:
            self.instance.previous_card = self.instance.card
            self.instance.previous_member = self.instance.member

        self.fields['card'].queryset = self.fields['card'].queryset.filter(associated_costume__isnull=True)
        if self.instance.card:
            self.fields['card'].queryset = self.fields['card'].queryset.filter(associated_costume=self.instance)

        self.fields['member'].help_text = _('If associating this costume with a card, you can leave this blank. I\'ll take the member from the card.')

        if not self.is_creating and self.instance.i_costume_type != models.Costume.COSTUME_TYPE_LIVE:
            self.fields['member'].help_text = ""
            del self.fields['card']

    def clean(self):
        cleaned_data = super(CostumeForm, self).clean()

        if cleaned_data.get('i_costume_type') != models.Costume.COSTUME_TYPE_LIVE:
            cleaned_data['card'] = None

        # We take the card's title, so return null.
        if not cleaned_data.get('card') and not cleaned_data.get('name'):
            raise forms.ValidationError('Costumes without associated cards must have a name.')
        elif cleaned_data.get('card'):
            cleaned_data['member'] = cleaned_data['card'].member
            cleaned_data['name'] = None

        return cleaned_data

    class Meta(AutoForm.Meta):
        model = models.Costume
        fields = '__all__'
        save_owner_on_creation = True

class CostumeFilterForm(MagiFiltersForm):
    # Encompasses people like the dads, chispa... etc.
    # since only the 25 main girls get real Member entries.
    ID_OF_MISC_MEMBERS = 0
    search_fields = ['name', 'card__japanese_name', 'card__name', 'member__name', 'member__japanese_name']
    ordering_fields = [
        ('id', _('ID')),
        ('name', _('Title')),
        ('member', _('Member')),
        ('i_costume_type', _('Costume type')),
    ]

    def _member_to_queryset(self, queryset, request, value):
        try:
            i = int(value)
        except ValueError:
            return queryset
        
        if i == self.ID_OF_MISC_MEMBERS:
            return queryset.filter(member__isnull=True)
        else:
            return queryset.filter(member__id=value)

    member = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])] + [(ID_OF_MISC_MEMBERS, 'Other')], initial=None, label=_('Member'))
    member_filter = MagiFilter(to_queryset=_member_to_queryset)

    class Meta(MagiFiltersForm.Meta):
        model = models.Costume
        fields = ('search', 'member', 'i_costume_type', 'ordering', 'reverse_order')

############################################################
# Single page form

class TeamBuilderForm(MagiFiltersForm):
    account = forms.ModelChoiceField(queryset=models.Account.objects.all(), empty_label=None)

    i_band = forms.ChoiceField(choices=BLANK_CHOICE_DASH + i_choices(models.Member.BAND_CHOICES), label=_('Band'), required=False)
    i_band_filter = MagiFilter(noop=True)

    i_attribute = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.Card.ATTRIBUTE_CHOICES, label=_('Attribute'), required=False)
    i_attribute_filter = MagiFilter(noop=True)

    i_skill_type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.Card.SKILL_TYPE_CHOICES, label=_('Skill'), required=False)
    i_skill_type_filter = MagiFilter(noop=True)

    perfect_accuracy = forms.IntegerField(label=_('How often do you hit PERFECT notes?'), widget=forms.NumberInput(attrs={
        'type':'range', 'step': '10', 'data-show-value': 'true', 'data-show-value-suffix': '%',
    }), initial=80, required=False)
    perfect_accuracy_filter = MagiFilter(noop=True)

    def clean_perfect_accuracy(self):
        return (self.cleaned_data.get('perfect_accuracy', 80) or 0) / 100

    stamina_accuracy = forms.IntegerField(label=_('How often is your life above 900?'), widget=forms.NumberInput(attrs={
        'type':'range', 'step': '10', 'data-show-value': 'true', 'data-show-value-suffix': '%',
    }), initial=80, required=False)
    stamina_accuracy_filter = MagiFilter(noop=True)

    def clean_stamina_accuracy(self):
        return (self.cleaned_data.get('stamina_accuracy', 80) or 0) / 100

    total_cards = forms.ChoiceField(required=False, label=_('Cards'), initial=5, choices=[
        (5, 5), (10, 10), (15, 15),
    ])
    total_cards_filter = MagiFilter(noop=True)

    def __init__(self, *args, **kwargs):
        super(TeamBuilderForm, self).__init__(*args, **kwargs)
        # If the user doesn't have an account, redirect to create account
        if len(getAccountIdsFromSession(self.request)) == 0:
            raise HttpRedirectException('/accounts/add/?next=/teambuilder/')
        # If the user has one account, hide the account selector
        elif len(getAccountIdsFromSession(self.request)) == 1:
            self.fields['account'] = HiddenModelChoiceField(queryset=self.fields['account'].queryset)
            self.fields['account'].initial = getAccountIdsFromSession(self.request)[0]
        # Otherwise, keep the selector but limit to the accounts owned by the authenticated user
        else:
            self.fields['account'].queryset = models.Account.objects.filter(owner=self.request.user)

    class Meta(MagiFiltersForm.Meta):
        model = models.CollectibleCard
        fields = ('account', 'i_band', 'i_attribute', 'i_skill_type')
        all_optional = False
