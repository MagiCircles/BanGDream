import datetime, os
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _, string_concat
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
            self.fields['center'].queryset = self.fields['center'].queryset.select_related('card')
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

    member_id = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])], required=False, label=_('Favorite Member'))
    member_id_filter = MagiFilter(selectors=['owner__preferences__favorite_character{}'.format(i) for i in range(1, 4)])

    has_friend_id = forms.NullBooleanField(required=False, initial=None, label=_('Friend ID'))
    has_friend_id_filter = MagiFilter(selector='friend_id__isnull')

    i_color = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(c[0], c[1]) for c in settings.USER_COLORS], required=False, label=_('Color'))
    i_color_filter = MagiFilter(selector='owner__preferences__color')

    class Meta(MagiFiltersForm.Meta):
        model = models.Account
        fields = ('search', 'friend_id', 'i_version', 'i_color', 'member_id', 'has_friend_id')

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
    search_fields = ['name', 'japanese_name', 'school', 'CV', 'romaji_CV', 'food_likes', 'food_dislikes', 'hobbies', 'description']

    ordering_fields = [
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
        return instance

    class Meta(AutoForm.Meta):
        model = models.Card
        fields = '__all__'
        save_owner_on_creation = True

class CardFilterForm(MagiFiltersForm):
    search_fields = ['_cache_j_member', 'name', 'japanese_name', 'skill_name', 'japanese_skill_name']
    ordering_fields = [
        ('release_date', _('Release date')),
        ('id', _('ID')),
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

    member_id = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])], initial=None, label=_('Member'))

    member_band = forms.ChoiceField(choices=BLANK_CHOICE_DASH + i_choices(models.Member.BAND_CHOICES), initial=None, label=_('Band'))
    member_band_filter = MagiFilter(selector='member__i_band')

    def _origin_to_queryset(self, queryset, request, value):
        if value == 'is_promo':
            return queryset.filter(is_promo=True)
        elif value == 'is_gacha':
            return queryset.filter(_cache_j_gachas__isnull=False)
        elif value == 'is_event':
            return queryset.filter(_cache_j_events__isnull=False)
        return queryset

    origin = forms.ChoiceField(label=_(u'Origin'), choices=BLANK_CHOICE_DASH + [
        ('is_event', _(u'Event')),
        ('is_gacha', _(u'Gacha')),
        ('is_promo', _(u'Promo')),
    ])
    origin_filter = MagiFilter(to_queryset=_origin_to_queryset)

    def _view_to_queryset(self, queryset, request, value):
        if value == 'chibis':
            return queryset.filter(_cache_chibis_ids__isnull=False).exclude(_cache_chibis_ids='')
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
        fields = ('view', 'search', 'member_id', 'member_band', 'i_rarity', 'i_attribute', 'origin', 'i_skill_type', 'member_band', 'version', 'ordering', 'reverse_order')

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

        member_id = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])], initial=None, label=_('Member'))
        member_id_filter = MagiFilter(selector='card__member_id')

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
            fields = ('search', 'member_id', 'member_band', 'i_rarity', 'i_attribute', 'i_skill_type', 'member_band', 'ordering', 'reverse_order', 'view')
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
        self.previous_main_card_id = None if self.is_creating else self.instance.main_card_id
        self.previous_secondary_card_id = None if self.is_creating else self.instance.secondary_card_id
        if 'c_versions' in self.fields:
            del(self.fields['c_versions'])

    def _clean_card_rarity(self, field_name, rarity):
        if field_name in self.cleaned_data and self.cleaned_data[field_name]:
            if self.cleaned_data[field_name].i_rarity != rarity:
                raise forms.ValidationError(u'Rarity must be {}'.format(rarity))
            return self.cleaned_data[field_name]
        return None

    def clean_main_card(self):
        return self._clean_card_rarity('main_card', 3)

    def clean_secondary_card(self):
        return self._clean_card_rarity('secondary_card', 2)

    def save(self, commit=False):
        instance = super(EventForm, self).save(commit=False)
        if instance.start_date:
            instance.start_date = instance.start_date.replace(hour=6, minute=00)
        if instance.end_date:
            instance.end_date = instance.end_date.replace(hour=11, minute=59)
        if instance.taiwanese_start_date:
            instance.taiwanese_start_date = instance.taiwanese_start_date.replace(hour=7, minute=00)
        if instance.taiwanese_end_date:
            instance.taiwanese_end_date = instance.taiwanese_end_date.replace(hour=13, minute=59)
        if instance.korean_start_date:
            instance.korean_start_date = instance.korean_start_date.replace(hour=6, minute=00)
        if instance.korean_end_date:
            instance.korean_end_date = instance.korean_end_date.replace(hour=13, minute=00)
        if self.previous_main_card_id != (instance.main_card.id if instance.main_card else 0):
            if instance.main_card:
                instance.main_card.force_update_cache('events')
            if self.previous_main_card_id:
                previous_card = models.Card.objects.get(id=self.previous_main_card_id)
                previous_card.force_update_cache('events')
        if self.previous_secondary_card_id != (instance.secondary_card.id if instance.secondary_card else 0):
            if instance.secondary_card:
                instance.secondary_card.force_update_cache('events')
            if self.previous_secondary_card_id:
                previous_card = models.Card.objects.get(id=self.previous_secondary_card_id)
                previous_card.force_update_cache('events')
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

class EventFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name']
    ordering_fields = [
        ('start_date', string_concat(_('Date'), ' (', _('Japanese version'), ')')),
        ('english_start_date', string_concat(_('Date'), ' (', _('English version'), ')')),
        ('taiwanese_start_date', string_concat(_('Date'), ' (', _('Taiwanese version'), ')')),
        ('korean_start_date', string_concat(_('Date'), ' (', _('Korean version'), ')')),
        ('name', _('Title')),
        ('japanese_name', string_concat(_('Title'), ' (', t['Japanese'], ')')),
    ]

    version = forms.ChoiceField(label=_(u'Server availability'), choices=BLANK_CHOICE_DASH + models.Account.VERSION_CHOICES)
    version_filter = MagiFilter(to_queryset=lambda form, queryset, request, value: queryset.filter(c_versions__contains=value))

    class Meta(MagiFiltersForm.Meta):
        model = models.Event
        fields = ('search', 'i_type', 'version', 'ordering', 'reverse_order')

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
        if 'c_versions' in self.fields:
            del(self.fields['c_versions'])

    def save(self, commit=False):
        instance = super(GachaForm, self).save(commit=False)
        if instance.start_date:
            instance.start_date = instance.start_date.replace(hour=6, minute=00)
        if instance.end_date:
            instance.end_date = instance.end_date.replace(hour=5, minute=59)
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

    is_limited = forms.NullBooleanField(initial=None, required=False, label=_('Limited'))
    is_limited_filter = MagiFilter(selector='limited')

    version = forms.ChoiceField(label=_(u'Server availability'), choices=BLANK_CHOICE_DASH + models.Account.VERSION_CHOICES)
    version_filter = MagiFilter(to_queryset=lambda form, queryset, request, value: queryset.filter(c_versions__contains=value))

    class Meta(MagiFiltersForm.Meta):
        model = models.Gacha
        fields = ('search', 'is_limited', 'version', 'ordering', 'reverse_order')

############################################################
# Played song

def to_PlayedSongForm(cls):
    class _PlayedSongForm(cls.form_class):
        class Meta(cls.form_class.Meta):
            optional_fields = ('score', 'screenshot')
    return _PlayedSongForm

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

class SongFilterForm(MagiFiltersForm):
    search_fields = ['japanese_name', 'romaji_name', 'name', 'composer', 'lyricist', 'arranger', 'c_unlock_variables']
    ordering_fields = [
        ('release_date', _('Release date')),
        ('japanese_name', _('Title')),
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
# Single page form

class TeamBuilderForm(MagiFiltersForm):
    account = forms.ModelChoiceField(queryset=models.Account.objects.all(), empty_label=None)

    i_band = forms.ChoiceField(choices=i_choices(models.Member.BAND_CHOICES), label=_('Band'))
    i_band_filter = MagiFilter(noop=True)

    i_attribute = forms.ChoiceField(choices=models.Card.ATTRIBUTE_CHOICES, label=_('Attribute'))
    i_attribute_filter = MagiFilter(noop=True)

    i_skill_type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.Card.SKILL_TYPE_CHOICES, label=_('Skill'), required=False)
    i_skill_type_filter = MagiFilter(noop=True)

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
