import time
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings as django_settings
from magi.tools import totalDonators, getStaffConfigurations
from bang import models

def generate_settings():

        print 'Get total donators'
        total_donators = totalDonators()

        print 'Get staff configurations'
        staff_configurations, latest_news = getStaffConfigurations()

        print 'Get the latest news'
        current_events = models.Event.objects.filter(end_date__gte=timezone.now())
        current_gacha = models.Gacha.objects.filter(end_date__gte=timezone.now())
        latest_news += [{
                'title': event.name,
                'image': event.image_url,
                'url': event.item_url,
                'hide_title': True,
                'ajax': event.ajax_item_url,
        } for event in current_events] + [{
                'title': gacha.name,
                'image': gacha.image_url,
                'url': gacha.item_url,
                'hide_title': True,
                'ajax': gacha.ajax_item_url,
        } for gacha in current_gacha]

        print 'Get the characters'
        all_members = models.Member.objects.all().order_by('name')
        favorite_characters = [(
            member.pk,
            member.name,
	    member.square_image_url,
        ) for member in all_members]

        print 'Get homepage characters'
        characters = models.Card.objects.filter(i_rarity=2).order_by('-release_date')[:2]
        homepage_characters = u','.join([u'\'{}\''.format(c.transparent_url) for c in characters])
        if len(characters) != 2:
                homepage_characters = ''
        if homepage_characters:
                homepage_characters = u'HOMEPAGE_CHARACTERS = [{}]'.format(homepage_characters)

        # print 'Get the starters'
        # all_starters = models.Card.objects.filter(pk__in=[100001, 200001, 300001]).order_by('pk')
        # starters = [(
        #         card.pk,
        #         card.cached_member.name,
        #         card.icon_url,
        # ) for card in all_starters]

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
' +  unicode(homepage_characters) + u'\n\
STAFF_CONFIGURATIONS = ' + unicode(staff_configurations) + u'\n\
FAVORITE_CHARACTERS = ' + unicode(favorite_characters) + u'\n\
MAX_STATS = ' + unicode(stats) + u'\n\
SCHOOLS = ' + unicode(schools) + '\n\
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
