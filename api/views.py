from rest_framework import viewsets, serializers
from web.item_model import get_http_image_url_from_path
from web import api_permissions
from web.utils import shrinkImageFromData
from bang import models

############################################################
# Fields

class ImageField(serializers.ImageField):
    def to_representation(self, value):
        return get_http_image_url_from_path(value)

class IField(serializers.IntegerField):
    def __init__(self, choices, *args, **kwargs):
        super(IField, self).__init__(*args, **kwargs)
        self.choices = choices
        self.reverse_choices = { v: k for k, v in choices.items() }

    def to_representation(self, value):
        return self.choices[value]

    def to_internal_value(self, data):
        return self.reverse_choices[data]

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
        for field, value in validated_data.items():
            # Optimize images with TinyPNG
            if type(self.Meta.model._meta.get_field(field)) == models.models.ImageField:
                value = getattr(instance, field)
                filename = value.name
                content = value.read()
                if not content:
                    setattr(instance, field, None)
                    continue
                image = shrinkImageFromData(content, filename, settings=getattr(self.Meta.model, 'tinypng_settings', {}).get(field, {}))
                image.name = self.Meta.model._meta.get_field(field).upload_to(instance, filename)
                setattr(instance, field, image)
        return instance

    def create(self, validated_data):
        self.is_creating = True
        validated_data = self._presave(validated_data)
        instance = self.Meta.model(**validated_data)
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
    i_band = IField(models.BAND_DICT)
    i_school_year = IField(models.ENGLISH_SCHOOL_YEAR_DICT, required=False)
    i_astrological_sign = IField(models.ENGLISH_ASTROLOGICAL_SIGN_DICT, required=False)

    class Meta:
        model = models.Member
        fields = ('id', 'name', 'japanese_name', 'image', 'square_image', 'i_band', 'school', 'i_school_year', 'romaji_CV', 'CV', 'birthday', 'food_likes', 'food_dislikes', 'i_astrological_sign', 'hobbies', 'description')
        save_owner_on_creation = True

class MemberViewSet(viewsets.ModelViewSet):
    queryset = models.Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = (api_permissions.IsStaffOrReadOnly, )

############################################################
# Card

class CardSerializer(MagiSerializer):
    i_attribute = IField(models.ENGLISH_ATTRIBUTE_DICT)
    i_skill_type = IField(models.ENGLISH_SKILL_TYPES_DICT)

    def validate(self, data):
        if self.context['request'].method == 'POST' and 'member' not in self.context['request'].data:
            raise serializers.ValidationError({
                'member': ['This field is required.'],
            })
        return data

    def _postsave(self, validated_data, instance):
        instance = super(CardSerializer, self)._postsave(validated_data, instance)
        instance.force_cache_member()
        return instance

    class Meta:
        model = models.Card
        save_owner_on_creation = True
        fields = ('id', 'member', 'i_rarity', 'i_attribute', 'image', 'image_trained', 'art', 'art_trained', 'transparent', 'transparent_trained', 'skill_name', 'japanese_skill_name', 'i_skill_type', 'skill_details', 'performance_min', 'performance_max', 'performance_trained_max', 'technique_min', 'technique_max', 'technique_trained_max', 'visual_min', 'visual_max', 'visual_trained_max')

class CardViewSet(viewsets.ModelViewSet):
    queryset = models.Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (api_permissions.IsStaffOrReadOnly, )
