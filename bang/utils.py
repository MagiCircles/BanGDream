import random, datetime
from collections import OrderedDict
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, get_language, string_concat
from django.db.models import Q
from magi.default_settings import RAW_CONTEXT
from magi.utils import (
    globalContext,
    toTimeZoneDateTime,
    toCountDown,
    staticImageURL,
    mergedFieldCuteForm,
    getCharacterImageFromPk,
)
from bang import models

def memberBandMergeCuteForm(cuteform):
    mergedFieldCuteForm(cuteform, {
        'title': string_concat(_('Member'), '/', _('Band')),
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    }, OrderedDict ([
        ('member', lambda k, v: getCharacterImageFromPk(int(k))),
        ('i_band', lambda k, v: staticImageURL(v, folder='band', extension='png')),
    ]))

def rarity_to_stars_images(rarity):
    return u'<img src="{static_url}img/star_{un}trained.png" alt="star">'.format(
        static_url=RAW_CONTEXT['static_url'],
        un='' if rarity in models.Card.TRAINABLE_RARITIES else 'un',
    ) * rarity

def generateDifficulty(difficulty):
    note_image = staticImageURL('note.png')
    return u'{big_images}{small_images}'.format(
        big_images=(u'<img src="{}" class="song-big-note">'.format(note_image) * (difficulty // 5)),
        small_images=(u'<img src="{}" class="song-small-note">'.format(note_image) * (difficulty % 5)),
    )

def bandField(band, i):
    return {
        'image': staticImageURL('mini_band_icon/{}.png'.format(band)),
        'verbose_name': _('Band'),
        'type': 'image_link',
        'link': u'/members/?i_band={}'.format(i),
        'ajax_link': u'/ajax/members/?i_band={}&ajax_modal_only'.format(i),
        'link_text': band,
        'value': staticImageURL('band/{}.png'.format(band)),
    }

# For Event, Gacha, Song
def subtitledImageLink(item, verbose_name, icon=None, image=None, subtitle=None):
    return {
        'image': image,
        'icon': icon,
        'verbose_name': verbose_name,
        'verbose_name_subtitle': subtitle or unicode(item),
        'value': (getattr(item, '{}image_url'.format(
            models.Account.VERSIONS[models.LANGUAGES_TO_VERSIONS.get(get_language(), 'EN')]['prefix'],
        ), None) or item.image_url),
        'type': 'image_link',
        'link': item.item_url,
        'ajax_link': item.ajax_item_url,
        'link_text': subtitle or unicode(item),
    }

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
                        toCountDown(date=rerun.end_date if rerun.status == 'current' else rerun.start_date,
                            sentence=_('{time} left') if rerun.status == 'current' else _('Starts in {time}'),
                            classes=['fontx1-5']),
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

############################################################
# In settings

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
    for popup_name, popup in context.get('corner_popups', {}).items():
        popup['image_overflow'] = True
        if popup_name == 'happy_birthday':
            popup['image'] = staticImageURL('birthday_kanae.png')
    return context

############################################################
# In settings, used when generating settings

def getBackgrounds():
    return [
        {
            'id': background.id,
            'thumbnail': background.top_image_list,
            'image': background.top_image,
            'name': background.name,
            'd_names': background.names,
        } for background in models.Asset.objects.filter(
            i_type=models.Asset.get_i('type', 'background'),
        ) if background.top_image
    ]

def getCurrentEventsAndGachas(versions=[]):
    now = timezone.now()
    two_days_ago = now - datetime.timedelta(days=2)
    in_twelve_days = now + datetime.timedelta(days=12) # = event length 7d + 5d margin
    return {
        version_name: [
            event
            for event in (list(
                    models.Event.objects.filter(**{
                        version['prefix'] + 'end_date__gte': two_days_ago,
                        version['prefix'] + 'end_date__lte': in_twelve_days,
                    })) + list(models.Gacha.objects.filter(**{
                        version['prefix'] + 'end_date__gte': now,
                        version['prefix'] + 'end_date__lte': in_twelve_days,
                    })))
        ] for version_name, version in models.Account.VERSIONS.items()
        if not versions or version_name in versions
    }

def getHomepageArts(
        only_recent_cards=True,
        only_for_character_id=None,
        only_card_ids=[],
        fallback_to_all=True,
        randomize=False,
        limit_to=20,
):
    now = timezone.now()

    # Get cards with allowed arts
    cards = models.Card.objects.exclude(
        (Q(art__isnull=True) | Q(art=''))
        & (Q(art_trained__isnull=True) | Q(art_trained=''))
        & (Q(transparent__isnull=True) | Q(transparent='')),
    ).exclude(
        show_art_on_homepage=False,
        show_trained_art_on_homepage=False,
    ).order_by('?' if randomize else '-release_date')

    filtered_cards = cards

    # Recent cards
    if only_recent_cards:
        # Events and gachas
        condition = Q()
        for version_name, events in getCurrentEventsAndGachas(versions=['JP', 'EN']).items():
            for event in events:
                if event._meta.model.__name__ == 'Gacha':
                    condition |= Q(gachas=event)
                else:
                    condition |= Q(secondary_card_event=event)
                    condition |= Q(main_card_event=event)
        # Or promo
        ten_days_ago = now - datetime.timedelta(days=10)
        condition |= Q(is_promo=True, release_date__gte=ten_days_ago)
        filtered_cards = filtered_cards.filter(condition)

    # Per character
    if only_for_character_id:
        filtered_cards = filtered_cards.filter(
            member_id=only_for_character_id,
        )

    # Cards ids
    if only_card_ids:
        filtered_cards = filtered_cards.filter(id__in=only_card_ids)

    # Fallback to all cards when no filtered cards
    if fallback_to_all and not filtered_cards:
        filtered_cards = cards
    else:
        filtered_cards = filtered_cards

    # Limit to
    if limit_to:
        filtered_cards = filtered_cards[:limit_to]

    # Transform to arts
    homepage_arts = []
    position = { 'size': 'cover', 'x': 'center', 'y': 'center' }
    for c in filtered_cards:
        # Normal
        if c.show_art_on_homepage:
            if c.trainable and c.art:
                homepage_arts.append({
                    'url': c.art_url,
                    'hd_url': c.art_2x_url or c.art_original_url,
                    'about_url': c.item_url,
                })
            elif c.transparent:
                homepage_arts.append({
                    'foreground_url': c.transparent_url,
                    'about_url': c.item_url,
                    'position': position,
                })
        # Trained
        if c.trainable and c.show_trained_art_on_homepage:
            if c.trainable and c.art_trained:
                homepage_arts.append({
                    'url': c.art_trained_url,
                    'hd_url': c.art_trained_2x_url or c.art_trained_original_url,
                    'about_url': c.item_url,
                })
            elif c.transparent_trained:
                homepage_arts.append({
                    'foreground_url': c.transparent_trained_url,
                    'about_url': c.item_url,
                    'position': position,
                })

    return homepage_arts

def randomArtForCharacter(character_id):
    try:
        return getHomepageArts(
            only_for_character_id=character_id,
            randomize=True,
            fallback_to_all=False,
            only_recent_cards=False,
        )[0]
    except:
        return None
