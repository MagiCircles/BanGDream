import time, datetime
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import get_language, activate as translation_activate, ugettext_lazy as _
from django.utils.formats import dateformat
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings as django_settings
from magi.tools import totalDonators, getStaffConfigurations, latestDonationMonth
from magi.utils import birthdays_within
from bang import models

def generate_settings():

    print 'Get total donators'
    total_donators = totalDonators() or '\'\''

    print 'Get latest donation month'
    donation_month = latestDonationMonth(failsafe=True)

    print 'Get staff configurations'
    staff_configurations, latest_news = getStaffConfigurations()

    print 'Get the latest news'
    now = timezone.now()
    old_lang = get_language()

    for member in  models.Member.objects.filter(
            birthdays_within(days_after=12, days_before=1, field_name='birthday')
    ):
        card = models.Card.objects.filter(member=member).filter(show_art_on_homepage=True).order_by('-i_rarity', '-release_date')[0]
        t_titles = {}
        for lang, _verbose in django_settings.LANGUAGES:
            translation_activate(lang)
            t_titles[lang] = u'{}, {}! {}'.format(
                _('Happy Birthday'),
                member.first_name,
                dateformat.format(member.birthday, 'F d'),
            )
        translation_activate(old_lang)
        latest_news.append({
            't_titles': t_titles,
            'background': card.art_original_url,
            'url': member.item_url,
            'hide_title': False,
            'ajax': False,
            'css_classes': 'birthday',
        })

    two_days_ago = now - datetime.timedelta(days=2)
    in_twelve_days = now + datetime.timedelta(days=12) # = event length 7d + 5d margin
    for version in models.Account.VERSIONS.values():
        for event in (list(
                models.Event.objects.filter(**{
                    version['prefix'] + 'end_date__gte': two_days_ago,
                    version['prefix'] + 'end_date__lte': in_twelve_days,
                })) + list(models.Gacha.objects.filter(**{
                    version['prefix'] + 'end_date__gte': now,
                    version['prefix'] + 'end_date__lte': in_twelve_days,
                }))):
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

    print 'Get the characters'
    all_members = models.Member.objects.all().order_by('id')
    favorite_characters = [(
        member.pk,
        member.name,
	    member.square_image_url,
    ) for member in all_members]

    print 'Get homepage cards'
    cards = models.Card.objects.exclude(Q(art__isnull=True) | Q(art='')).exclude(i_rarity=1).exclude(show_art_on_homepage=False, show_trained_art_on_homepage=False).order_by('-release_date')[:5]
    homepage_cards = []
    for c in cards:
        if c.show_art_on_homepage:
            homepage_cards.append({
                'art_url': c.art_url,
                'hd_art_url': c.art_2x_url or c.art_original_url,
                'item_url': c.item_url,
            })
        if c.art_trained and c.show_trained_art_on_homepage:
            homepage_cards.append({
                'art_url': c.art_trained_url,
                'hd_art_url': c.art_trained_2x_url or c.art_trained_original_url,
                'item_url': c.item_url,
            })

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

    print 'Save generated settings'
    # STARTERS = ' + unicode(starters) + u'\n\
    s = u'\
# -*- coding: utf-8 -*-\n\
import datetime\n\
LATEST_NEWS = ' + unicode(latest_news) + u'\n\
TOTAL_DONATORS = ' + unicode(total_donators) + u'\n\
DONATION_MONTH = ' + unicode(donation_month) + u'\n\
HOMEPAGE_CARDS = ' +  unicode(homepage_cards) + u'\n\
STAFF_CONFIGURATIONS = ' + unicode(staff_configurations) + u'\n\
FAVORITE_CHARACTERS = ' + unicode(favorite_characters) + u'\n\
MAX_STATS = ' + unicode(stats) + u'\n\
SCHOOLS = ' + unicode(schools) + u'\n\
GENERATED_DATE = datetime.datetime.fromtimestamp(' + unicode(time.time()) + u')\n\
'
    print s
    with open(django_settings.BASE_DIR + '/' + django_settings.SITE + '_project/generated_settings.py', 'w') as f:
        f.write(s.encode('utf8'))
        f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        generate_settings()
