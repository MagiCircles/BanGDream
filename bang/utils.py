from magi.default_settings import RAW_CONTEXT
from bang import models
#from bang.model_choices import TRAINABLE_RARITIES

def rarity_to_stars_images(rarity):
    return u'<img src="{static_url}img/star_{un}trained.png" alt="star">'.format(
        static_url=RAW_CONTEXT['static_url'],
        un='' if rarity in models.Card.TRAINABLE_RARITIES else 'un',
    ) * rarity
