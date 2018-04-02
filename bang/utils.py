from magi.default_settings import RAW_CONTEXT
from django.utils.translation import get_language
from magi.utils import globalContext
from bang import models
#from bang.model_choices import TRAINABLE_RARITIES

FONTS_PER_LANGUAGE = {
    'zh-hans': {
        'name': 'Noto Sans SC',
        'url': '//fonts.googleapis.com/earlyaccess/notosanssc.css',
        'title_weight': 800,
    },
    'zh-hant': {
        'name': 'Noto Sans TC',
        'url': '//fonts.googleapis.com/earlyaccess/notosanstc.css',
        'title_weight': 800,
    },
    'kr': {
        'name': 'Nanum Gothic',
        'url': '//fonts.googleapis.com/css?family=Nanum+Gothic:400,800',
        'title_weight': 800,
    },
    'ja': {
        'name': 'Rounded Mplus 1c',
        'url': '//fonts.googleapis.com/earlyaccess/roundedmplus1c.css',
        'title_weight': 900,
    },
    'ru': {
        'name': 'Comfortaa',
        'url': '//fonts.googleapis.com/css?family=Comfortaa:400',
        'title_url': '//fonts.googleapis.com/css?family=Exo+2:800',
        'title': 'Exo 2',
        'title_weight': 800,
    },
}

TITLE_CSS_CLASSES = 'h1, h2, h3, h4, h5, h6, .title, .navbar-brand, .btn-lg, .btn-xl'

def bangGlobalContext(request):
    context = globalContext(request)
    # Change font depending on language
    if context['current_language'] in FONTS_PER_LANGUAGE:
        f = FONTS_PER_LANGUAGE[context['current_language']]
        if 'name' in f and 'url' in f:
            context['extracss'] = context.get('extracss', '') + u'\n        @import url({url});{title_url}\n\
        body {{ font-family: \'{name}\', sans-serif; }}\n        {css_classes} {{ font-family: \'{title_name}\', monospace;{title_weight} }}'.format(
                url=f['url'],
                title_url=(u'\n@import url({url});'.format(url=f['title_url']) if 'title_url' in f else ''),
                name=f['name'],
                css_classes=TITLE_CSS_CLASSES,
                title_name=f.get('title', f['name']),
                title_weight=(u' font-weight: {weight};'.format(weight=f['title_weight'])
                              if 'title_weight' in f else ''),
            )
        if 'teko_title' in f:
            context['extracss'] = context.get('extracss', '') + u'\n        @import url(//fonts.googleapis.com/css?family=Teko:700);\n\
        {css_classes} {{ font-family: \'Teko\', sans-serif; font-weight: bold; font-style: italic; }}'.format(css_classes=TITLE_CSS_CLASSES)
    return context

def rarity_to_stars_images(rarity):
    return u'<img src="{static_url}img/star_{un}trained.png" alt="star">'.format(
        static_url=RAW_CONTEXT['static_url'],
        un='' if rarity in models.Card.TRAINABLE_RARITIES else 'un',
    ) * rarity
