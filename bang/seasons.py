import random, json
from django.conf import settings as django_settings
from magi.settings import (
    HOMEPAGE_BACKGROUNDS,
)
from bang.utils import (
    getHomepageArts,
)

def getRandomChristmasArt():
    homepage_arts = []
    try:
        homepage_arts += getHomepageArts(
            only_card_ids=django_settings.STAFF_CONFIGURATIONS.get('christmas_theme_cards', '').split(','),
            only_recent_cards=False,
            fallback_to_all=False,
            randomize=True,
            limit_to=1,
        )
    except:
        pass
    try:
        arts = json.loads(django_settings.STAFF_CONFIGURATIONS.get('christmas_theme_arts', [])) or []
        random.shuffle(arts)
        homepage_arts += [arts[0]]
    except:
        pass
    if homepage_arts:
        return random.choice(homepage_arts)
    return None

def getRandomChristmasBackground():
    try:
        return random.choice([
            background
            for background in HOMEPAGE_BACKGROUNDS
            if background['id'] in [
                    int(id)
                    for id in django_settings.STAFF_CONFIGURATIONS.get(
                            'christmas_theme_backgrounds', '').split(',')
            ]
        ])
    except IndexError:
        return None

def getRandomPrideBackground():
    return {
        'image': u'pride{}.png'.format(random.randint(1, 5)),
    }
