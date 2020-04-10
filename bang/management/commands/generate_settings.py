# -*- coding: utf-8 -*-
from django.utils.translation import activate as translation_activate, get_language
from magi import urls # needed to load static_url
from magi.tools import (
    generateSettings,
    listUnique,
)
from bang import models
from bang.utils import (
    getCurrentEventsAndGachas,
)

def generate_settings():

    ############################################################
    # BanG Dream!

    print 'Get schools'
    schools = listUnique(models.Member.objects.filter(school__isnull=False).values_list('school', flat=True).distinct())

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

    ############################################################
    # Girls Band Party

    # Events & Gachas
    print 'Add events and gachas to latest news'
    latest_news = []
    old_lang = get_language()
    for version_name, events in getCurrentEventsAndGachas().items():
        version = models.Account.VERSIONS[version_name]
        for event in events:
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

    ############################################################

    print 'Save generated settings'
    generateSettings({
        'LATEST_NEWS': latest_news,
        'MAX_STATS': stats,
        'SCHOOLS': schools,
        'AREAS': areas,
    })
