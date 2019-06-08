# -*- coding: utf-8 -*-
import datetime, random
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import get_language, activate as translation_activate, ugettext_lazy as _
from magi import urls # needed to load static_url
from magi.tools import (
    generateSettings,
    totalDonatorsThisMonth,
    getStaffConfigurations,
    latestDonationMonth,
    getCharactersBirthdays,
    getUsersBirthdaysToday,
)
from magi.utils import (
    staticImageURL,
    birthdays_within,
)
from bang import models

def generate_settings():

    print 'Get total donators'
    total_donators = totalDonatorsThisMonth() or '\'\''

    print 'Get latest donation month'
    donation_month = latestDonationMonth(failsafe=True)

    print 'Get staff configurations'
    staff_configurations, latest_news = getStaffConfigurations()

    print 'Get the latest news'
    now = timezone.now()
    old_lang = get_language()

    # Birthdays

    def get_name_image_url_from_character(character):
        card = models.Card.objects.filter(member=character).filter(
            show_art_on_homepage=True).order_by('-i_rarity', '-release_date')[0]
        return character.first_name, card.art_original_url, character.item_url

    latest_news = getCharactersBirthdays(
        models.Member.objects.all(),
        get_name_image_url_from_character,
        latest_news=latest_news,
    )

    # Users birthdays
    latest_news = getUsersBirthdaysToday(
        staticImageURL('happy_birthday.png'),
        latest_news=latest_news,
        max_usernames=4,
    )

    # Events & Gachas

    two_days_ago = now - datetime.timedelta(days=2)
    in_twelve_days = now + datetime.timedelta(days=12) # = event length 7d + 5d margin
    events_with_cards = []
    for version_name, version in models.Account.VERSIONS.items():
        for event in (list(
                models.Event.objects.filter(**{
                    version['prefix'] + 'end_date__gte': two_days_ago,
                    version['prefix'] + 'end_date__lte': in_twelve_days,
                })) + list(models.Gacha.objects.filter(**{
                    version['prefix'] + 'end_date__gte': now,
                    version['prefix'] + 'end_date__lte': in_twelve_days,
                }))):
            if version_name in ['JP', 'EN']:
                events_with_cards.append(event)
            image = getattr(event, u'{}image_url'.format(version['prefix']))
            if not image:
                continue
            translation_activate(version['code'])
            latest_news.append({
                'title': unicode(event.t_name),
                'image': image,
                'url': event.item_url,
                'hide_title': True,
                'ajax': False, #event.ajax_item_url, weird carousel bug with data-ajax
            })
        translation_activate(old_lang)

    # User Profile Backgrounds
    print 'Get the backgrounds'
    background_choices = models.Asset.objects.filter(
        i_type=models.Asset.get_i('type', 'background'))

    backgrounds = [
        {
            'id': background.id,
            'thumbnail': background.top_image_list,
            'image': background.top_image,
            'name': background.name,
            'd_names': background.names,
        } for background in background_choices if background.top_image]

    print 'Get the characters'
    all_members = models.Member.objects.all().order_by('id')
    favorite_characters = [(
        member.pk,
        member.name,
	member.square_image_url,
    ) for member in all_members]

    print 'Get homepage cards'
    cards = models.Card.objects.exclude(
        (Q(art__isnull=True) | Q(art=''))
        & (Q(art_trained__isnull=True) | Q(art_trained=''))
        & (Q(transparent__isnull=True) | Q(transparent='')),
    ).exclude(
        show_art_on_homepage=False,
        show_trained_art_on_homepage=False,
    ).order_by('-release_date')

    is_character_birthday = False
    birthday_today_members_id = models.Member.objects.filter(
        birthdays_within(days_after=1, days_before=1)).values_list(
            'id', flat=True)
    if birthday_today_members_id:
        filtered_cards = cards.filter(member_id__in=birthday_today_members_id)[:20]
        is_character_birthday = True
    else:
        condition = Q()
        for event in events_with_cards:
            if event._meta.model.__name__ == 'Gacha':
                condition |= Q(gachas=event)
            else:
                condition |= Q(secondary_card_event=event)
                condition |= Q(main_card_event=event)
        ten_days_ago = now - datetime.timedelta(days=10)
        condition |= Q(is_promo=True, release_date__gte=ten_days_ago)
        filtered_cards = cards.filter(condition)

    if filtered_cards:
        filtered_cards = filtered_cards[:20]
    else:
        filtered_cards = cards[:10]
        is_character_birthday = False

    homepage_arts = []
    position = { 'size': 'cover', 'x': 'center', 'y': 'center' }
    pride_backgrounds = [
        staticImageURL(u'pride{}.png'.format(i))
        for i in range(1, 6)
    ]
    for c in filtered_cards:
        # Normal
        if c.show_art_on_homepage:
            if c.trainable and c.art and False:
                homepage_arts.append({
                    'url': c.art_url,
                    'hd_url': c.art_2x_url or c.art_original_url,
                    'about_url': c.item_url,
                })
            elif c.transparent:
                homepage_arts.append({
                    'url': random.choice(pride_backgrounds),
                    'foreground_url': c.transparent_url,
                    'side': ['left', 'right'],
                    'about_url': c.item_url,
                    'position': position,
                })
        # Trained
        if c.trainable and c.show_trained_art_on_homepage:
            if c.trainable and c.art_trained and False:
                homepage_arts.append({
                    'url': c.art_trained_url,
                    'hd_url': c.art_trained_2x_url or c.art_trained_original_url,
                    'about_url': c.item_url,
                })
            elif c.transparent_trained:
                homepage_arts.append({
                    'url': random.choice(pride_backgrounds),
                    'foreground_url': c.transparent_trained_url,
                    'side': ['left', 'right'],
                    'about_url': c.item_url,
                    'position': position,
                })
    if not homepage_arts:
        homepage_arts = [{
            'url': '//i.bandori.party/u/c/art/838Kasumi-Toyama-Happy-Colorful-Poppin-U7hhHG.png',
            'hd_url': '//i.bandori.party/u/c/art/838Kasumi-Toyama-Happy-Colorful-Poppin-WV6jFP.png',
        }]

    print 'Get max stats'
    stats = {
        'performance_max': None,
        'performance_trained_max': None,
        'technique_max': None,
        'technique_trained_max': None,
        'visual_max': None,
        'visual_trained_max': None,
        'overall_max_': None,
        'overall_trained_max_': None,
    }
    try:
        for stat in stats.keys():
            max_stats = models.Card.objects.all().extra(select={
                'overall_max_': 'performance_max + technique_max + visual_max',
                'overall_trained_max_': 'performance_trained_max + technique_trained_max + visual_trained_max',
            }).order_by('-' + stat)[0]
            stats[stat] = getattr(max_stats, stat)
        stats['overall_max'] = stats['overall_max_']
        del(stats['overall_max_'])
        stats['overall_trained_max'] = stats['overall_trained_max_']
        del(stats['overall_trained_max_'])
    except IndexError:
        pass

    print 'Get schools'
    schools = models.Member.objects.filter(school__isnull=False).values_list('school', flat=True).distinct()

    print 'Get areas'
    areas = [
        {
            'id': area.id,
            'image': area.image_url,
            'name': area.name,
            'd_names': area.names,
        }
        for area in models.Area.objects.all()
    ]

    print 'Save generated settings'

    generateSettings({
        'LATEST_NEWS': latest_news,
        'TOTAL_DONATORS': total_donators,
        'DONATION_MONTH': donation_month,
        'HOMEPAGE_ARTS': homepage_arts,
        'IS_CHARACTER_BIRTHDAY': is_character_birthday,
        'STAFF_CONFIGURATIONS': staff_configurations,
        'FAVORITE_CHARACTERS': favorite_characters,
        'BACKGROUNDS': backgrounds,
        'MAX_STATS': stats,
        'SCHOOLS': schools,
        'AREAS': areas,
    })

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        generate_settings()
