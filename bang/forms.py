import datetime
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _, string_concat
from django.utils.safestring import mark_safe
from django.db.models.fields import BLANK_CHOICE_DASH
from django import forms
from web.utils import join_data
from web.forms import MagiForm, AutoForm, MagiFiltersForm, MagiFilter
from bang import settings
from bang.django_translated import t
from bang import models

############################################################
# Accounts

class AccountForm(MagiForm):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        if self.is_creating:
            del(self.fields['start_date'])

    def clean_start_date(self):
        if 'start_date' in self.cleaned_data:
            if self.cleaned_data['start_date']:
                if self.cleaned_data['start_date'] < datetime.date(2017, 3, 16):
                    raise forms.ValidationError(_('The game didn\'t even exist at that time.'))
                if self.cleaned_data['start_date'] > datetime.date.today():
                    raise forms.ValidationError(_('This date cannot be in the future.'))
        return self.cleaned_data['start_date']

    class Meta:
        model = models.Account
        fields = ('level', 'friend_id', 'start_date')
        optional_fields = ('level', 'friend_id', 'start_date')

class FilterAccounts(MagiFiltersForm):
    search_fields = ['owner__username', 'owner__preferences__description', 'owner__preferences__location']
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
    # has_friend_id_filter = MagiFilter(selector='friend_id__isnull') This will work with latest magicircles when merging
    def _filter_friend_id(self, queryset, request, value):
        if value == '2':
            value = True
        elif value == '3':
            value = False
        else:
            value = None
        return queryset.filter(friend_id__isnull=not value) if value is not None else queryset
    has_friend_id_filter = MagiFilter(to_queryset=_filter_friend_id)

    i_attribute = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(c[0], c[1]) for c in settings.USER_COLORS], required=False, label=_('Attribute'))
    i_attribute_filter = MagiFilter(selector='owner__preferences__color')

    class Meta:
        model = models.Account
        fields = ('search', 'friend_id', 'i_attribute', 'member_id', 'has_friend_id', )

############################################################
# Member

class MemberForm(AutoForm):
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        # Change labels for staff
        self.fields['square_image'].label = 'Small icon (for the map)'
        self.fields['square_image'].help_text = mark_safe('Example: <img src="https://i.bandori.party/u/i/m/1Toyama-Kasumi-D7Fpvu.png" height="40">')

    class Meta:
        model = models.Member
        fields = '__all__'
        save_owner_on_creation = True
        optional_fields = ('band', 'school', 'i_school_year', 'CV', 'romaji_CV', 'birthday', 'food_likes', 'food_dislikes', 'i_astrological_sign', 'hobbies', 'description')

class MemberFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name', 'school', 'CV', 'romaji_CV', 'food_likes', 'food_dislikes', 'hobbies', 'description']

    ordering_fields = [
        ('_cache_total_fans', _('Popularity')),
        ('name', _('Name')),
        ('japanese_name', string_concat(_('Name'), ' (', t['Japanese'], ')')),
        ('birthday', _('Birthday')),
    ]

    school = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(s, s) for s in getattr(django_settings, 'SCHOOLS', [])], initial=None)

    class Meta:
        model = models.Member
        fields = ('search', 'i_band', 'school', 'i_school_year', 'i_astrological_sign')

############################################################
# Card

class CardForm(AutoForm):
    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        self.previous_member_id = None if self.is_creating else self.instance.member_id
        self.fields['skill_details'].label = 'Skill details'
        self.fields['side_skill_details'].label = 'Side skill details'

    def save(self, commit=False):
        instance = super(CardForm, self).save(commit=False)
        if self.previous_member_id != instance.member_id:
            instance.update_cache_member()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Card
        fields = '__all__'
        save_owner_on_creation = True
        optional_fields = ('name', 'japanese_name', 'image_trained', 'art_trained', 'transparent_trained', 'skill_name', 'japanese_skill_name', 'skill_details', 'i_side_skill_type', 'side_skill_details', 'school', 'i_school_year', 'CV', 'romaji_CV', 'birthday', 'food_likes', 'food_dislikes', 'i_astrological_sign', 'hobbies', 'description', 'performance_trained', 'technique_trained', 'visual_trained', 'chibi')

class CardFilterForm(MagiFiltersForm):
    search_fields = ['_cache_member_name', '_cache_member_japanese_name', 'name', 'japanese_name', 'skill_name', 'japanese_skill_name']
    ordering_fields = [
        ('id', _('ID')),
        ('_cache_member_name', string_concat(_('Member'), ' - ', _('Name'))),
        ('_cache_member_japanese_name', string_concat(_('Member'), ' - ', _('Name'), ' (', t['Japanese'], ')')),
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

    def _trainable_to_queryset(form, queryset, request, value):
        if value == '2':
            return queryset.filter(i_rarity__in=models.TRAINABLE_RARITIES)
        elif value == '3':
            return queryset.exclude(i_rarity__in=models.TRAINABLE_RARITIES)
        return queryset

    trainable = forms.NullBooleanField(initial=None, required=False, label=_('Trainable'))
    trainable_filter = MagiFilter(to_queryset=_trainable_to_queryset)
    member_id = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])], initial=None, label=_('Member'))
    member_band = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.BAND_CHOICES, initial=None, label=_('Band'))
    member_band_filter = MagiFilter(selector='member__i_band')

    class Meta:
        model = models.Card
        fields = ('search', 'member_id', 'member_band', 'i_rarity', 'i_attribute', 'trainable', 'i_skill_type', 'i_side_skill_type', 'member_band', 'ordering', 'reverse_order')

############################################################
# Event

class EventForm(AutoForm):
    start_date = forms.DateField(label=_('Beginning'))
    end_date = forms.DateField(label=_('End'))

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.previous_main_card_id = None if self.is_creating else self.instance.main_card_id
        self.previous_secondary_card_id = None if self.is_creating else self.instance.secondary_card_id

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
            instance.start_date = instance.start_date.replace(hour=5, minute=59)
        if instance.end_date:
            instance.end_date = instance.end_date.replace(hour=11, minute=59)
        if self.previous_main_card_id != (instance.main_card.id if instance.main_card else 0):
            if instance.main_card:
                instance.main_card.update_cache_event()
            if self.previous_main_card_id:
                previous_card = models.Card.objects.get(id=self.previous_main_card_id)
                previous_card.update_cache_event()
        if self.previous_secondary_card_id != (instance.secondary_card.id if instance.secondary_card else 0):
            if instance.secondary_card:
                instance.secondary_card.update_cache_event()
            if self.previous_secondary_card_id:
                previous_card = models.Card.objects.get(id=self.previous_secondary_card_id)
                previous_card.update_cache_event()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Event
        fields = '__all__'
        optional_fields = ('start_date', 'end_date', 'rare_stamp', 'stamp_translation', 'main_card', 'secondary_card', 'i_boost_attribute', 'boost_members')
        save_owner_on_creation = True

class EventFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name']
    ordering_fields = [
        ('start_date', _('Date')),
        ('name', _('Name')),
        ('japanese_name', string_concat(_('Name'), ' (', t['Japanese'], ')')),
    ]

    class Meta:
        model = models.Event
        fields = ('search', 'ordering', 'reverse_order')

############################################################
# Gacha

class GachaForm(AutoForm):
    start_date = forms.DateField(label=_('Beginning'))
    end_date = forms.DateField(label=_('End'))

    def save(self, commit=False):
        instance = super(GachaForm, self).save(commit=False)
        if instance.start_date:
            instance.start_date = instance.start_date.replace(hour=5, minute=59)
        if instance.end_date:
            instance.end_date = instance.end_date.replace(hour=5, minute=59)
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Gacha
        fields = '__all__'
        optional_fields = ('cards', 'event')
        save_owner_on_creation = True

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

    class Meta:
        model = models.Song
        fields = '__all__'
        optional_fields = ('length', 'bpm', 'easy_notes', 'easy_difficulty', 'normal_notes', 'normal_difficulty', 'hard_notes', 'hard_difficulty', 'expert_notes', 'expert_difficulty', 'name', 'romaji_name', 'itunes_id', 'composer', 'lyricist', 'arranger', 'release_date')
        save_owner_on_creation = True

def unlock_to_form(unlock):
    class _UnlockSongForm(_SongForm):
        def __init__(self, *args, **kwargs):
            super(_UnlockSongForm, self).__init__(*args, **kwargs)
            help_text = mark_safe(u'Will be displayed as <code>{}</code>'.format(
                unicode(models.UNLOCK_SENTENCES[unlock]).format(**{
                    variable: 'xxx'
                    for variable in models.UNLOCK_VARIABLES[unlock]
                }),
            )) if unlock != 'other' else None
            for i, variable in enumerate(models.UNLOCK_VARIABLES[unlock]):
                self.fields[variable] = forms.CharField(
                    help_text=help_text,
                    initial=None if self.is_creating else self.instance.unlock_variables[i],
                )
            if unlock != 'event' and 'event' in self.fields:
                del(self.fields['event'])

        def save(self, commit=False):
            instance = super(_UnlockSongForm, self).save(commit=False)
            instance.i_unlock = next(k for k, v in models.UNLOCK_DICT.items() if v == unlock)
            instance.c_unlock_variables = join_data(*[
                self.cleaned_data[variable]
                for variable in models.UNLOCK_VARIABLES[unlock]
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

    def _is_cover_queryset(form, queryset, request, value):
        if value == '2':
            return queryset.filter(is_cover=True)
        elif value == '3':
            return queryset.filter(is_cover=False)
        return queryset

    is_cover = forms.NullBooleanField(initial=None, required=False, label=_('Cover'))
    is_cover_filter = MagiFilter(to_queryset=_is_cover_queryset)

    class Meta:
        model = models.Song
        fields = ('search', 'i_band', 'i_unlock', 'is_cover', 'ordering', 'reverse_order')
