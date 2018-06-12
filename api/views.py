from rest_framework import viewsets, serializers, permissions
from magi.item_model import get_http_image_url_from_path
from magi import api_permissions
from magi.utils import shrinkImageFromData, join_data
from bang import models

############################################################
# Fields

class FileField(serializers.FileField):
    def to_representation(self, value):
        return get_http_image_url_from_path(value)

class ImageField(serializers.ImageField):
    def to_representation(self, value):
        return get_http_image_url_from_path(value)

class IField(serializers.IntegerField):
    def __init__(self, model, field_name, *args, **kwargs):
        super(IField, self).__init__(*args, **kwargs)
        self._model = model
        self._field_name = field_name

    def to_representation(self, value):
        return self._model.get_reverse_i(self._field_name, value)

    def to_internal_value(self, data):
        return self._model.get_i(self._field_name, data)

class IFieldManualChoices(serializers.IntegerField):
    def __init__(self, choices, *args, **kwargs):
        super(IFieldManualChoices, self).__init__(*args, **kwargs)
        self.choices = choices
        self.reverse_choices = { v: k for k, v in choices.items() }

    def to_representation(self, value):
        return self.choices[value]

    def to_internal_value(self, data):
        return self.reverse_choices[data]

class CField(serializers.ListField):
    child = serializers.CharField()

    def __init__(self, model, field_name, translated=True, *args, **kwargs):
        super(CField, self).__init__(*args, **kwargs)
        self._model = model
        self._field_name = field_name
        self._translated = translated

    def to_internal_value(self, data):
        return join_data(*data)

    def to_representation(self, value):
        return self._model.get_csv_values(self._field_name, value, translated=self._translated)

############################################################
# Serializer

class MagiSerializer(serializers.ModelSerializer):
    def _presave(self, validated_data):
        if self.is_creating and getattr(self.Meta, 'save_owner_on_creation', False):
            validated_data['owner'] = self.context['request'].user
        for k, v in validated_data.items():
            if v == '':
                validated_data[k] = None
        return validated_data

    def _postsave(self, validated_data, instance):
        need_save = False
        for field, value in validated_data.items():
            # Optimize images with TinyPNG
            if type(self.Meta.model._meta.get_field(field)) == models.models.ImageField:
                need_save = True
                if (hasattr(self.Meta, 'tinypng_on_save')
                    and field in self.Meta.tinypng_on_save
                ):
                    value = getattr(instance, field)
                    filename = value.name
                    content = value.read()
                    if not content:
                        setattr(instance, field, None)
                        continue
                    image = shrinkImageFromData(content, filename, settings=getattr(self.Meta.model, 'tinypng_settings', {}).get(field, {}))
                    image.name = self.Meta.model._meta.get_field(field).upload_to(instance, filename)
                    setattr(instance, field, image)
                else:
                    # Remove any cached processed image
                    setattr(instance, u'_tthumbnail_{}'.format(field), None)
                    setattr(instance, u'_thumbnail_{}'.format(field), None)
                    setattr(instance, u'_original_{}'.format(field), None)
                    setattr(instance, u'_2x_{}'.format(field), None)
        if need_save:
            instance.save()
        return instance

    def create(self, validated_data):
        self.is_creating = True
        validated_data = self._presave(validated_data)
        m2m = getattr(self.Meta, 'many_to_many_fields', [])
        validated_data_without_m2m = {
            k: v for k, v in validated_data.items()
            if k not in m2m
        }
        instance = self.Meta.model(**validated_data_without_m2m)
        instance.save()
        if m2m:
            for field_name in m2m:
                setattr(instance, field_name, validated_data[field_name])
            instance.save()
        return self._postsave(validated_data, instance)

    def update(self, instance, validated_data):
        self.is_creating = False
        validated_data = self._presave(validated_data)
        instance = super(MagiSerializer, self).update(instance, validated_data)
        return self._postsave(validated_data, instance)

############################################################
# Member

class MemberSerializer(MagiSerializer):
    image = ImageField()
    square_image = ImageField()
    i_band = IField(models.Member, 'band')
    i_school_year = IField(models.Member, 'school_year', required=False)
    i_astrological_sign = IField(models.Member, 'astrological_sign', required=False)

    class Meta:
        model = models.Member
        fields = ('id', 'name', 'japanese_name', 'image', 'square_image', 'i_band', 'school', 'i_school_year', 'romaji_CV', 'CV', 'birthday', 'food_like', 'food_dislike', 'i_astrological_sign', 'instrument', 'description')
        save_owner_on_creation = True

class MemberViewSet(viewsets.ModelViewSet):
    queryset = models.Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = (api_permissions.IsStaffOrReadOnly, )

class MemberIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ('id',)

class MemberIDViewSet(viewsets.ModelViewSet):
    queryset = models.Member.objects.all().values('id')
    serializer_class = MemberIDSerializer
    paginate_by = None

    def list(self, request):
        r = super(MemberIDViewSet, self).list(request)
        r.data = [member['id'] for member in r.data]
        return r

############################################################
# Card

class CardSerializer(MagiSerializer):
    i_attribute = IFieldManualChoices({ _value: _a['english'] for _value, _a in models.Card.ATTRIBUTES.items() })
    i_skill_type = IFieldManualChoices({ _value: _a['english'] for _value, _a in models.Card.SKILL_TYPES.items() }, required=False)
    i_side_skill_type = IFieldManualChoices({ _value: _a['english'] for _value, _a in models.Card.SKILL_TYPES.items() }, required=False)
    image = ImageField(required=False)
    image_trained = ImageField(required=False)
    art = ImageField(required=False)
    art_trained = ImageField(required=False)
    transparent = ImageField(required=False)
    transparent_trained = ImageField(required=False)

    def validate(self, data):
        if self.context['request'].method == 'POST' and 'member' not in self.context['request'].data:
            raise serializers.ValidationError({
                'member': ['This field is required.'],
            })
        return data

    def _postsave(self, validated_data, instance):
        instance = super(CardSerializer, self)._postsave(validated_data, instance)
        if self.context['request'].method != 'POST':
            instance.update_cache("member")
            instance.update_cache("cameos")
        return instance

    class Meta:
        model = models.Card
        save_owner_on_creation = True
        many_to_many_fields = ('cameo_members',)
        fields = (
            'id', 'member', 'i_rarity', 'i_attribute', 'name', 'japanese_name', 'release_date',
            'is_promo', 'is_original',
            'image', 'image_trained', 'art', 'art_trained', 'transparent', 'transparent_trained',
            'skill_name', 'japanese_skill_name', 'i_skill_type', 'i_side_skill_type',
            # Not editable
            'skill_template', 'skill_variables', 'side_skill_template', 'side_skill_variables', 'full_skill',
            # / Not editable
            'performance_min', 'performance_max', 'performance_trained_max',
            'technique_min', 'technique_max', 'technique_trained_max',
            'visual_min', 'visual_max', 'visual_trained_max', 'cameo_members'
        )

class CardSerializerForEditing(CardSerializer):
    i_skill_special = IField(models.Card, 'skill_special', required=False)
    i_skill_note_type = IField(models.Card, 'skill_note_type', required=False)

    class Meta(CardSerializer.Meta):
        fields = CardSerializer.Meta.fields + (
            'i_skill_special',
            'i_skill_note_type', 'skill_stamina', 'skill_duration', 'skill_percentage', 'skill_alt_percentage',
        )

class CardViewSet(viewsets.ModelViewSet):
    queryset = models.Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (api_permissions.IsStaffOrReadOnly, )

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return CardSerializerForEditing
        return CardSerializer

class CardIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Card
        fields = ('id',)

class CardIDViewSet(viewsets.ModelViewSet):
    queryset = models.Card.objects.all().values('id')
    serializer_class = CardIDSerializer
    paginate_by = None

    def list(self, request):
        r = super(CardIDViewSet, self).list(request)
        r.data = [card['id'] for card in r.data]
        return r

############################################################
# Event

class EventSerializer(MagiSerializer):
    image = ImageField(required=True)
    i_type = IField(models.Event, 'type')
    c_versions = CField(models.Event, 'versions', translated=False)
    english_image = ImageField(required=False)
    taiwanese_image = ImageField(required=False)
    korean_image = ImageField(required=False)
    rare_stamp = ImageField(required=False)
    i_boost_attribute = IFieldManualChoices({ _value: _a['english'] for _value, _a in models.Card.ATTRIBUTES.items() }, required=False)

    class Meta:
        model = models.Event
        save_owner_on_creation = True
        many_to_many_fields = ('boost_members',)
        fields = (
            'image', 'name', 'japanese_name', 'i_type', 'start_date', 'end_date', 'c_versions',
            'english_image', 'english_start_date', 'english_end_date',
            'taiwanese_image', 'taiwanese_start_date', 'taiwanese_end_date',
            'korean_image', 'korean_start_date', 'korean_end_date',
            'rare_stamp', 'stamp_translation',
            'main_card', 'secondary_card',
            'i_boost_attribute', 'boost_members',
        )

class EventViewSet(viewsets.ModelViewSet):
    queryset = models.Event.objects.all().prefetch_related('boost_members')
    serializer_class = EventSerializer
    permission_classes = (api_permissions.IsStaffOrReadOnly, )

############################################################
# Costume

class CostumeSerializer(MagiSerializer):
    i_costume_type = IField(models.Costume, 'costume_type', required=True)

    class Meta:
        model = models.Costume
        save_owner_on_creation = True
        fields = (
            'id', 'i_costume_type', 'member', 'card', 'resolved_preview_image', 'name'
        )

class CostumeSerializerForEditing(CostumeSerializer):
    model_pkg = FileField(required=True)
    preview_image = ImageField(required=False)

    def validate(self, data):
        if not data.get('card'):
            if not data.get('name'):
                raise serializers.ValidationError({
                    'name': ['Costumes without associated cards must have a name.'],
                })
            if not data.get('preview_image'):
                raise serializers.ValidationError({
                    'name': ['Costumes without associated cards must have a preview image.'],
                })
        else:
            data['member'] = data['card'].member
            data['name'] = None
        return data

    class Meta(CostumeSerializer.Meta):
        fields = CostumeSerializer.Meta.fields + ('model_pkg', 'preview_image')

class CostumeViewSet(viewsets.ModelViewSet):
    queryset = models.Costume.objects.all()
    serializer_class = CostumeSerializer
    permission_classes = (api_permissions.IsStaffOrReadOnly, )

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return CostumeSerializerForEditing
        return CostumeSerializer
