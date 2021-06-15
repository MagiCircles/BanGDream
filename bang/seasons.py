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

def getRandomPrideArt():
    r = random.choice([
        {
            'url': 'https://i.imgur.com/fdmnbra.png',
            'about_url': 'https://bandori.party/activity/49615/here-s-another-edit-i-made-all-the-guitarists-excluding-touko-and-lock-rip-wishing-you-a-happy/',
        },
        {
            'url': 'https://i.imgur.com/nMwz2I7.png',
            'about_url': 'https://bandori.party/activity/49603/Lesbian-PAREO-3-I-think-the-edit-is-a-little-ugly-but-I-m-happy-with-the-result/',
        },
        {
            'url': 'https://i.imgur.com/Bg3BJTj.png',
            'about_url': 'https://bandori.party/activity/49598/Shhhhh-mods-are-asleep-it-s-time-to-post-last-minute-entries-Sorry-if-it-s-bad-i-don-t/',
        },
        {
            'url': 'https://i.imgur.com/8r3QZtV.jpg',
            'about_url': 'https://bandori.party/activity/49597/Hello-I-am-new-here-but-am-I-late-with-the-Pride-Month-card-event-In-this-one-I-made-Omni/',
        },
        {
            'foreground_url': 'https://i.imgur.com/6snXIo8.jpg',
            'about_url': 'https://bandori.party/activity/49585/i-did-another-one-color-red-g-color-color-orange-a-color-color-yellow-y-color/',
        },
        {
            'url': 'https://i.imgur.com/uZtTmQM.jpg',
            'about_url': 'https://bandori.party/activity/49584/I-made-this-pan-Pareo-edit-and-it-took-me-longer-than-what-I-expected-But-I-m-not-disappointed/',
        },
        {
            'url': 'https://i.bandori.party/u/activities/azKpO3idCtYPbwap4Co8LbDI7tlYAY.jpg',
            'about_url': 'https://bandori.party/activity/49580/this-took-me-surprisingly-long-and-uhhh-it-s-not-even-that-good-but-anyway/',
        },
        {
            'foreground_url': 'https://i.bandori.party/u/activities/MEecPE9BmENCgLInGZr8eGqStMtjP0.png',
            'about_url': 'https://bandori.party/activity/49568/happy-pride-month-sorry-if-my-handwriting-doesn-t-look-good-everyone-had-such-good-edits-that/',
        },
        {
            'url': 'https://i.bandori.party/u/activities/NsMmFmRWmZRx59AxlQkEVyXRBzQeXa.png',
            'about_url': 'https://bandori.party/activity/49565/New-day-More-pride-edits-Pride-buttons-Straight-ally-Moca-Asexual-Bi-romantic-Ran-Other/',
        },
        {
            'url': 'https://i.bandori.party/u/activities/kXVgKQ9kDUvuzRolaAWpARh5OpipNl.png',
            'about_url': 'https://bandori.party/activity/49556/My-last-edit-for-today-Here-s-Masking-rocking-some-nonbinary-pride-Happy-pride-month/',
        },
        {
            'foreground_url': 'https://i.bandori.party/u/activities/btn9PiBq74msHFdbUfCRnIfJyzEQtR.png',
            'about_url': 'https://bandori.party/activity/49554/Pan-pride-Kaoru-I-did-another-costume-color-edit-This-time-it-s-Kaoru-representing-some/',
        },
        {
            'foreground_url': 'https://i.bandori.party/u/activities/NluGRScGQD7A3izI7TTy70gGP6ymfj.jpeg',
            'about_url': 'https://bandori.party/activity/49552/Happy-pride-month-Headcanon-that-hina-is-asekual-since-she-is-friendlikely-to-all-girls-and-her/',
        },
        {
            'url': 'https://i.bandori.party/u/activities/wQm3KdwrLHV2w0miPBYunJu2jUcj5Q.png',
            'about_url': 'https://bandori.party/activity/49551/I-don-t-know-how-to-use-this-website-but-happy-pride-month-3/',
        },
        {
            'foreground_url': 'https://i.bandori.party/u/activities/3G2kTrW2yfOEqnh1l1ftNSpO84wDxC.png',
            'about_url': 'https://bandori.party/activity/49547/This-is-the-last-one-I-swear-I-just-got-too-excited-Anyway-are-Bandorisona-edits-still-a-thing/',
        },
        {
            'foreground_url': 'https://i.bandori.party/u/activities/4W7G9LnyRSuZ3TNSYK3pM2B6w1zsLb.png',
            'about_url': 'https://bandori.party/activity/49537/Happy-pride-month/',
        },
        {
            'url': 'https://i.bandori.party/u/activities/jZS4Jb9VmmyDMSCqzQETGfHzJIyC2S.png',
            'about_url': 'https://bandori.party/activity/49531/An-asexual-spectrum-edit-of-Rui-I-really-wanted-to-edit-the-Morfonica-outfit-with-ace-colors-and/',
        },
        {
            'url': 'https://i.bandori.party/u/activities/F6NoBO9A6VBGwtR8y7hG94fmPu3zTM.png',
            'about_url': 'https://bandori.party/activity/49520/Anyone-for-rainbow-bread/',
        },
        {
            'url': 'https://i.bandori.party/u/activities/a0NCm7JQQoPLIEMcGfsXgBhVolxGGn.png',
            'about_url': 'https://bandori.party/activity/49517/okay-this-took-a-little-longer-than-i-thought-but-here-s-my-card-edit-so-i-headcanon-hina-to-be-a/',
        },
        {
            'foreground_url': 'https://i.bandori.party/u/activities/tTt6pEL8EXwmK5310aNc5l09qcQuir.png',
            'about_url': 'https://bandori.party/activity/49516/Happy-Pride-Month-I-ve-always-wanted-to-edit-Mizuki-into-a-bandori-card-so-heres-Mizuki/',
        },
        {
            'foreground_url': 'https://i.bandori.party/u/activities/AB6NMPF8XhizdznvamQPJuhPbBCdqa.jpg',
            'about_url': 'https://bandori.party/activity/49515/Hello-judges-and-may-I-say-you-re-looking-great-today-My-Pride-edit-is-ass-but-hey-it-s/',
        },
        {
            'url': 'https://i.bandori.party/u/activities/cagm01cVMiNCYf4SPL1n6jYxo8wo9p.png',
            'about_url': 'https://bandori.party/activity/49511/Heya-Happy-Pride-I-wouldn-t-consider-myself-as-part-of-the-lgbtq-spectrum-tbh-but-it-s-kinda-a/',
        },
        {
            'url': 'https://i.bandori.party/u/activities/jdjWuDyyOjNENGvM1I1GcgNxS7NvOh.png',
            'about_url': 'https://bandori.party/activity/49509/HEYYY-happy-PrideMonth-everyone-flags-transfem-bisexual-genderfluid/',
        },
        {
            'foreground_url': 'https://i.bandori.party/u/activities/YZkYTftJSAz2XJeFnZhrcqYkW522ig.png',
            'about_url': 'https://bandori.party/activity/49508/am-not-very-the-best-of-editing-but-i-tried-my-best-with-this-challenge-happy-pride-month/',
        },
        {
            'url': 'https://i.bandori.party/u/activities/mYn8MHmSVeY5Giw0ysUNilGqnsLfnY.jpeg',
            'about_url': 'https://bandori.party/activity/49507/I-m-not-that-good-at-edits-but-here-s-my-submission-to-the-PRIDE-Ready-event-Non-binary/',
        },
        {
            'foreground_url': 'https://i.bandori.party/u/activities/8SmjTsNaEmpNyHvGxv4OrbUGkEey3G.jpg',
            'about_url': 'https://bandori.party/activity/49504/PrideMonth-To-celebrate-Pride-Month-along-with-RAS-debut-on-EN-server-coming-soon-I/',
        },
        {
            'foreground_url': 'https://i.bandori.party/u/activities/wV3IlIzXXmKfofylCs96LRVxN1c8oE.png',
            'about_url': 'https://bandori.party/activity/49496/Hihi-Happy-Pride-Month-She-just-conveniently-happened-to-be-holding-a-flag/',
        },
        {
            'url': 'https://i.bandori.party/u/activities/htAUstbawnXTHsBBPXEuM4StvhhaD9.png',
            'about_url': 'https://bandori.party/activity/49494/Rinko-wishes-you-a-happy-pride-month/',
        },
        {
            'url': 'https://i.bandori.party/u/activities/QyruNHtonbPWU9nb9MiijZAJ4SMpBY.png',
            'about_url': 'https://bandori.party/activity/49493/lesbian-pride-tomoe-for-the-pride-ready-event/',
        },
        {
            'foreground_url': 'https://i.bandori.party/u/activities/7VxccwbrXslO6zaDvrWwvpeecfwiw0.png',
            'about_url': 'https://bandori.party/activity/49488/oh-we-postin-pride-edits-Pareo-s-perfect-for-this-made-this-one-a-while-ago-it-potentially/',
        },
        {
            'url': 'https://i.bandori.party/u/activities/E95o0p21uhxtdtWPk1PfuWOxP0zgrl.jpeg',
            'about_url': 'https://bandori.party/activity/49717/The-Pride-Ready-event-may-be-over-but-will-I-still-make-edits-You-bet-I-will-So-here-s-Pan/',
        },
    ])
    return r
