from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, get_language
from magi.default_settings import RAW_CONTEXT
from magi.utils import globalContext, toTimeZoneDateTime, toCountDown, staticImageURL
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
    'vi': {
        'name': 'Montserrat',
        'url': '//fonts.googleapis.com/css?family=Montserrat:400,700',
        'title_weight': 700,
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
    return context

def rarity_to_stars_images(rarity):
    return u'<img src="{static_url}img/star_{un}trained.png" alt="star">'.format(
        static_url=RAW_CONTEXT['static_url'],
        un='' if rarity in models.Card.TRAINABLE_RARITIES else 'un',
    ) * rarity

def generateDifficulty(difficulty):
    note_image = staticImageURL('note.png')
    val = '{big_images}{small_images}'.format(
        big_images=(u'<img src="{}" class="song-big-note">'.format(note_image) * (difficulty // 5)),
        small_images=(u'<img src="{}" class="song-small-note">'.format(note_image) * (difficulty % 5)),
    )
    return val

def add_rerun_buttons(view, buttons, request, item):
    if request.user.is_authenticated() and request.user.hasPermission('manage_main_items'):
        for version in item.versions:
            i_version = models.Rerun.get_i('version', version)
            buttons[u'{}add_rerun'.format(models.Rerun.VERSIONS[version]['prefix'])] = {
                'classes': view.item_buttons_classes + ['staff-only'],
                'show': True,
                'url': u'/reruns/add/?{item}_id={item_id}&i_version={i_version}'.format(
                    item=type(item).__name__.lower(),
                    item_id=item.id,
                    i_version=i_version,
                ),
                'icon': 'date',
                'title': u'Add rerun dates in {}'.format(models.Rerun.get_verbose_i('version', i_version)),
                'has_permissions': True,
                'open_in_new_window': True,
            }
    return buttons

def add_rerun_fields(view, item, request):
    extra_fields = []
    if len(item.all_reruns):
        for rerun in item.all_reruns:
            extra_fields.append(('{}rerun'.format(rerun.version_prefix), {
                'icon': 'date',
                'verbose_name': _('Rerun'),
                'type': 'html',
                'value': u'<p>{}</p>'.format(u'</p><p>'.join([
                    unicode(x) for x in [
                        toCountDown(rerun.start_date, _('Starts in {time}')) if rerun.status == 'future' else None,
                        toCountDown(rerun.end_date, _('{time} left')) if rerun.status == 'current' else None,
                        u'<strong>{}</strong>'.format(_('Beginning')) if rerun.start_date else None,
                        toTimeZoneDateTime(rerun.start_date, [rerun.version_timezone, 'Local time'], ago=True),
                        u'<strong>{}</strong>'.format(_('End')) if rerun.end_date else None,
                        toTimeZoneDateTime(rerun.end_date, [rerun.version_timezone, 'Local time'], ago=True),
                        u'<a href="{edit_url}" class="{classes}">{edit_sentence}</a>'.format(
                            edit_url=rerun.edit_url,
                            classes=u' '.join(view.item_buttons_classes + ['staff-only']),
                            edit_sentence=rerun.edit_sentence,
                        ) if (request
                              and request.user.is_authenticated()
                              and request.user.hasPermission('manage_main_items'))
                        else None,
                    ] if x
                ])),
            }))
    return extra_fields
