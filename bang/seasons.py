# -*- coding: utf-8 -*-
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

PRIDE_ARTS = [
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
    {
        'about_url': u'https://bandori.party/activity/54276/Happy-Pride-Month-Here-s-Tsugumi-wearing-some-Bisexual-pride-colors-Hope-everyone-can-enjoy/',
        'url': u'https://i.bandori.party/u/activities/0cUmlZ7b4aDpxCyE2nZsgPtTSRJPzW.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54267/Happy-pride-month-Here-is-edit-of-my-favorite-card-of-PAREO-I-have-never-done-an-edit-before-but/',
        'url': u'https://i.bandori.party/u/activities/h1GrUghPXboQVhj65ksCiodd3aZpoC.jpg',
    },
    {
        'about_url': u'https://bandori.party/activity/54266/These-outfits-are-just-so-perfect-bandori-knows-what-s-up-lol-Also-I-saw-the-art-of-Tae-and/',
        'url': u'https://i.bandori.party/u/activities/9HIuyDbuBM3hzwPfcYXKVYRB4yinvj.jpeg',
    },
    {
        'about_url': u'https://bandori.party/activity/54265/2-pride-edits-in-one-day-It-s-more-likely-than-you-think-Tae-wearing-some-demigirl-pride-colors/',
        'url': u'https://i.bandori.party/u/activities/Ww8aU0WrQurs3RZd4cTSJRXqx8r1HG.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54264/Sayo-wearing-some-Aromantic-Pride-Happy-Pride-Month/',
        'url': u'https://i.bandori.party/u/activities/YzBDwoZBgSQGFTXI5gtar3i7rmcFnu.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54263/idk-how-this-website-works-but-i-made-a-few-pride-edits-like-earlier-and-found-out-there-s-an-event/',
        'foreground_url': u'https://i.bandori.party/u/activities/QwukoClpMoWRA5Rv0CVnkbXAUmyYF6.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54262/EXPLAIN-BANDORI-PARTY-You-promised-that-all-participants-of-the-pride-ready-event-would-get-a/',
        'foreground_url': u'https://i.bandori.party/u/activities/GIBj5bQ0Ssn1YIDsEUoCUINTewdEeV.PNG',
    },
    {
        'about_url': u'https://bandori.party/activity/54261/Во-чё-наделала-всех-с-гордым-месяцом/',
        'url': u'https://i.bandori.party/u/activities/CEHMForphaZdsn6jLnXgAUHTYxW6gE.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54260/panmoca-i-imgur-com-126An7w-png-what-do-you-mean-this-isn-t-the-original-card/',
        'url': u'https://camo.githubusercontent.com/7e403422fabe942be20fe00ce226b30e48e27bb6b54bbd092c1fa0b9b7be2031/68747470733a2f2f692e696d6775722e636f6d2f313236416e37772e706e67',
    },
    {
        'about_url': u'https://bandori.party/activity/54257/Aw-yeah-it-s-Tomoe-wooo-I-had-to-get-a-little-creative-with-this-one-because-I-m-starting-to/',
        'url': u'https://i.bandori.party/u/activities/E7WUHObpBmpWHbFlo9WL03r8TiSb7y.jpeg',
    },
    {
        'about_url': u'https://bandori.party/activity/54256/I-didn-t-even-have-to-do-anything-It-already-shows-transgender-PAREO-she-already-has-all-the/',
        'foreground_url': u'https://i.bandori.party/u/activities/2bf8HredGjg3HKFziE7uDUFO252T0K.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54255/HAPPY-PRIDE-MONTH-It-might-not-rlly-be-easy-to-see-bc-my-mom-can-see-my-photo-gallery-and-idk-if/',
        'url': u'https://i.bandori.party/u/activities/9HSjEfR1bqmmny69I7UgrZ18d2IoDq.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54254/Lesbian-chisato-My-headcanon-is-she-is-married-with-kanon/',
        'url': u'https://i.bandori.party/u/activities/EoRo0pkVEA0ksPAxcvXE7u4nRKse9E.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54253/I-retried-my-pride-month-thing/',
        'url': u'https://i.bandori.party/u/activities/p7rS4d0hu8y2C70vTIvbVrZhY4myek.jpg',
    },
    {
        'about_url': u'https://bandori.party/activity/54251/Nanami-for-the-win-lol-I-ve-started-to-mix-up-the-way-that-I-edit-the-cards-because-if-I-add/',
        'url': u'https://i.bandori.party/u/activities/lG0RgQreJS0sZyz0pRK6DKicz5yzxU.jpeg',
    },
    {
        'about_url': u'https://bandori.party/activity/54250/Choose-your-fighter-flag-sorry-Hagumi-for-hiding-your-face/',
        'url': u'https://i.bandori.party/u/activities/iKCGHl5eeRG0aZRqjTEayf33vyzMRJ.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54244/This-will-be-the-last-edit-I-ll-make-for-the-event-And-now-I-introduce-you-Bi-Himari/',
        'url': u'https://i.bandori.party/u/activities/okC4UyauYRP8r2Af54xL15cTFuzOJU.jpg',
    },
    {
        'about_url': u'https://bandori.party/activity/54241/extremely-lazy-himari-edit-bc-i-hc-her-as-a-raging-bisexual/',
        'url': u'https://i.bandori.party/u/activities/lNy9nSJYNKWLVoq42BHD4qCWJHhb7p.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54237/Happy-pride-month-3/',
        'url': u'https://i.bandori.party/u/activities/x4FHdP4Y2v5UYSaYXdpqTgcHVVrihA.jpg',
    },
    {
        'about_url': u'https://bandori.party/activity/54235/heyo-here-s-a-uh-proper-pride-post/',
        'url': u'https://camo.githubusercontent.com/e9c573b49c411ba3c8ec00c7be2d7f980c9a3681ffd53a06cb5a805cd9a28c3d/68747470733a2f2f692e62616e646f72692e70617274792f752f616374697669746965732f325466646454374d375650683964623263726a70664757534f41324b71592e706e67',
    },
    {
        'about_url': u'https://bandori.party/activity/54232/Edits-go-brrrrrrrrrrrrrr-That-s-all-I-have-to-say-at-this-point-lol-I-ve-run-out-of-comments/',
        'url': u'https://i.bandori.party/u/activities/o3urAbKF1pnpuxcjMtWtPTwiWLPE0K.jpeg',
    },
    {
        'about_url': u'https://bandori.party/activity/54230/Pride-supporting-idol-Maruyama-Aya-desu-彡-Happy-Pride-Month/',
        'url': u'https://i.bandori.party/u/activities/hXxq7iXo3vMB9rsx3KP5kdaMaVsreF.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54229/Happy-Pride-Month-Here-s-my-submission-for-the-PRIDE-Ready-event-It-doesn-t-look-the-best/',
        'url': u'https://i.bandori.party/u/activities/7Mx2t8UvipgppIrtLmj9pb1L5PmA1f.jpg',
    },
    {
        'about_url': u'https://bandori.party/activity/54220/Moreeee-head-canons-Wahahaha-I-know-that-it-s-kinda-stupid-that-I-put-a-watermark-on-the/',
        'url': u'https://i.bandori.party/u/activities/dyOLWaitqlc6my9S8Ysd6hVaYoh79g.jpeg',
    },
    {
        'about_url': u'https://bandori.party/activity/54214/hi-everyone-this-is-my-first-post-here-i-m-new-to-bandori-i-absolutely-love-pareo/',
        'url': u'https://i.bandori.party/u/activities/m8uofRvvMQxkpn7O0Ker2jkWQ7KRlt.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54213/Happy-Pride-Month-Here-we-have-Maya-sporting-some-genderfluid-pride-colors-More-coming-soon/',
        'url': u'https://i.bandori.party/u/activities/bLVITTQpq36WBpzrPWRVGBxZZVGiLa.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54211/my-friend-saw-this-event-and-wanted-to-do-an-edit-so-here-it-is-a-bi-Rinko-edit/',
        'url': u'https://i.bandori.party/u/activities/PPGnm2tUj4k5TnNUyGOMQqKJoPODSK.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54209/Another-edit-for-Pride-month-and-this-time-it-s-Pareo-Yes-I-used-one-of-her-2-star-cards-and/',
        'url': u'https://i.bandori.party/u/activities/tizAqDAZnucoaNRAJTFthsykfsQiwo.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54203/This-edit-s-a-little-more-lazy-than-the-last-one-but-enjoy-I-added-her-signature-to-make/',
        'url': u'https://i.bandori.party/u/activities/u7HlP7hsY2gzyJ3DiCTFSwARwvnett.jpeg',
    },
    {
        'about_url': u'https://bandori.party/activity/54192/unlabeled-bride-maya-that-i-kinda-made-for-my-partner-lmao/',
        'url': u'https://i.bandori.party/u/activities/vVTOJLxaQrySebTedRwQcZeHGrXBIV.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54191/HAPPY-PRIDE-MONTHHHH-I-grant-you-all-this-years-edit-PANSEXUAL-MOCA-AOBA/',
        'url': u'https://i.bandori.party/u/activities/JWOWX2oBRWTWxr4VTpr6fBefsGUDxc.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54190/I-never-edited-something-before-so-it-might-look-ugly-Welp-practice-makes-perfect/',
        'url': u'https://i.bandori.party/u/activities/KckyzeYH44yBcy5Ut95PEgP8gIasGY.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54189/I-heard-pride-ready-2022-I-had-to-do-the-sequel-to-bi-Ako-coming-out-and-what-I-originally/',
        'url': u'https://i.bandori.party/u/activities/SfF9OsFsNQo3jWHOZT0vBaL1PUI4VU.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54186/she-is-so-adorable/',
        'url': u'https://i.bandori.party/u/activities/KUauSQd70jrDdTbaot6GDlgMzngB4Y.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54185/I-once-again-do-the-pride-card-edits-but-this-time/',
        'url': u'https://i.bandori.party/u/activities/NUCFZtP7IXTuhZvON17YTQrDebCkJB.jpeg',
    },
    {
        'about_url': u'https://bandori.party/activity/54184/Happy-pride-month-everyone/',
        'url': u'https://i.bandori.party/u/activities/NQAYnMmlS1BmuHIMSUXAyeh9SqLIs8.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54178/Happy-Pride-Month/',
        'url': u'https://i.bandori.party/u/activities/7KIyL6SwvrQZfgUOig13AJscVFUo6Z.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54175/Second-edit-of-the-month-Mwahaha-I-think-that-even-though-the-contest-ends-on-the-tenth/',
        'url': u'https://i.bandori.party/u/activities/P5xl3r5D7D4VbcAMsGJq3OIsOfLjtS.jpeg',
    },
    {
        'about_url': u'https://bandori.party/activity/54174/idc-if-im-one-day-late-BUT-HAPPY-PRIDE-MONTH-GAYSS-Anyways-haruhapi-best-lesbians/',
        'url': u'https://i.bandori.party/u/activities/P4PHS3yx8fdRhIrxCRYulYmgto576C.jpg',
    },
    {
        'about_url': u'https://bandori.party/activity/54173/BanG-Dream-but-gayer/',
        'url': u'https://i.bandori.party/u/activities/UhwUTQbpZGQdUATDuP4bTLALbWzQsn.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54171/i-transed-pareo/',
        'url': u'https://i.bandori.party/u/activities/oEE9QBJ1FBQKIE0Fh6B7IPR9QvDjAX.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54165/shooba-hooba-here-s-Ummm-more-flag-colour-picks-hoo-hoo-kanon-trans-lesbian/',
        'url': u'https://camo.githubusercontent.com/369b7be7203a95a4027222521c2400efc03907ac0cd0749c21f08ca88ff2c0a3/68747470733a2f2f692e62616e646f72692e70617274792f752f616374697669746965732f7a6a53616534443571327936615774476f4e3130656743384564693146482e706e67',
    },
    {
        'about_url': u'https://bandori.party/activity/54165/shooba-hooba-here-s-Ummm-more-flag-colour-picks-hoo-hoo-kanon-trans-lesbian/',
        'url': u'https://camo.githubusercontent.com/38637cebd206835deb74af542b0abe8456a2e0d473db827c99012460e5eb7dd7/68747470733a2f2f692e62616e646f72692e70617274792f752f616374697669746965732f69714861324c7968356542377a4f354d7746786d653271703739496364352e706e67',
    },
    {
        'about_url': u'https://bandori.party/activity/54165/shooba-hooba-here-s-Ummm-more-flag-colour-picks-hoo-hoo-kanon-trans-lesbian/',
        'url': u'https://camo.githubusercontent.com/dc4e48f64aca81feb969bdef0a630650d154c2eba7c1582e9cf701db0859e89b/68747470733a2f2f692e62616e646f72692e70617274792f752f616374697669746965732f6c743951493436704a67656f686b454c38394969586f6f4c5136756847562e706e67',
    },
    {
        'about_url': u'https://bandori.party/activity/54161/agender-lesbian-moca-edit/',
        'url': u'https://i.bandori.party/u/activities/eipY7cSYNl2D0mwUGT2SPSM6rnyN1M.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54160/nb-chu2-edit/',
        'url': u'https://i.bandori.party/u/activities/htK2EhDWDnNLhEKuEJvKDZjHX4zVe5.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54154/IIIIIIIIT-S-PRIDE-MONTH-WOOOO-I-ve-had-this-edit-in-my-photos-for-over-a-little-while/',
        'url': u'https://i.bandori.party/u/activities/hKCvKRGmqUKIxXClDNs1i4dhuBbRaB.jpeg',
    },
    {
        'about_url': u'https://bandori.party/activity/54153/hi-banpa-hope-you-all-behave-this-month-here-is-the-nonbinary-lesbian-flags-colourpicked/',
        'url': u'https://i.bandori.party/u/activities/KxvIGgIHKscmfqchcdGkumexEEuz0e.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54152/Here-s-a-WIP-of-my-Lesbian-Kaoru-edit-Kaoru-is-one-of-my-favorite-characters-and-Kaoru-is-heavily/',
        'url': u'https://i.bandori.party/u/activities/0L88Fixa6f5HWgy3m7pX1xSoEwHXzk.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54144/Most-colorful-month-of-the-year-let-s-gooooo/',
        'url': u'https://i.bandori.party/u/activities/G8NQcgoyyyxqQdu1d8bmewvQLXfhBK.png',
    },
    {
        'about_url': u'https://bandori.party/activity/54143/It-s-that-time-again-Take-this-quick-edit-of-Rinko-And-yes-I-headcanon-her-as-asexual/',
        'url': u'https://i.bandori.party/u/activities/wEskHoZuXVGhMs8MWT0ERnC2EevvkI.jpg',
    },
    {
        'about_url': u'https://bandori.party/activity/54141/lil-maya-edit-for-pride-month-not-only-do-i-hc-her-as-a-lesbian-i-also-see-her-as-a-trans-girl-3/',
        'url': u'https://i.bandori.party/u/activities/DilX2VNJ27VJMtk4BNwN3UWPC8SsRL.png',
    },
]

def getPrideArts():
    print 'called?'
    return PRIDE_ARTS

def getRandomPrideArt():
    return random.choice(PRIDE_ARTS)
