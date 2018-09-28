# -*- coding: utf-8 -*-
from __future__ import division
import requests, json, sys, os, cStringIO, io
from PIL import Image
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.temp import NamedTemporaryFile
from django.core.files.images import ImageFile
from django.utils.six.moves import input
from magi import urls # Unused, fills up RAW_CONTEXT for file uploading
from magi.utils import dataToImageFile
from magi import models as magi_models
from bang import models

PARTS_SEPARATORS_PER_VERSION = {
    'JP': [u'①', u'②', u'③', u'④', u'⑤', u'⑥', u'⑦', u'⑧', u'⑨'],
    'EN': ['"'],
    'TW': [u'①', u'②', u'③', u'④', u'⑤', u'⑥', u'⑦', u'⑧', u'⑨'],
    'KR': [u'①', u'②', u'③', u'④', u'⑤', u'⑥', u'⑦', u'⑧', u'⑨'],
}

CHARACTER_OR_BAND_SEPARATORS_PER_VERSION = {
    'JP': [u'＆'],
    'EN': [u'&'],
    'TW': [u'＆', '&'],
    'KR': [u'&'],
}

BAND_ALT_NAMES = {
    u'ポピパ': 'Poppin\'Party',
    u'Popipa': 'Poppin\'Party',
    u'팝핀파': 'Poppin\'Party',
    u'パスパレ': 'Pastel*Palettes',
    u'Pastel＊Palettes': 'Pastel*Palettes',
    u'파스파레': 'Pastel*Palettes',
    u'ハロハピ': 'Hello, Happy World!',
    u'헬로해피': 'Hello, Happy World!',
}

ALT_MEMBER_NAMES = {
    u'ミッシェル': 'Misaki Okusawa',
    u'米歇爾': 'Misaki Okusawa',
    u'미셸': 'Misaki Okusawa',
    u'Saya': 'Saaya Yamabuki',
    u'上原 緋瑪麗': 'Himari Uehara',
    u'緋瑪麗': 'Himari Uehara',
    u'冰川纱夜': 'Sayo Hikawa',
    u'冰川紗夜': 'Sayo Hikawa',
    u'紗夜': 'Sayo Hikawa',
    u'纱夜': 'Sayo Hikawa',
}

VERSIONS_NEED_RESIZE = ['EN', 'TW', 'KR']

def get_owner():
    try:
        owner = models.User.objects.get(username='db0')
    except ObjectDoesNotExist:
        owner = models.User.objects.create(username='db0')
        preferences = magi_models.UserPreferences.objects.create(user=owner)
    return owner

def find_existing_comic_by_name(comics_in_db, language, comic_name):
    for comic in comics_in_db:
        name = comic.names.get(language, None)
        if name == comic_name:
            return comic
        if (name == comic_name.replace(u'…?', u'…')
            or name == comic_name.replace(u'...', u'…')
            or name == comic_name.replace('?', '')
        ):
            return comic
    return None

def find_member_from_name_or_partial_name(all_members, name, version):
    language = models.VERSIONS_TO_LANGUAGES[version]
    for member in all_members:
        member_name = member.name if language == 'en' else (
            member.japanese_name if language == 'ja' else
            member.names.get(language, member.name))
        if not member_name:
            continue
        member_name = member_name.strip()
        if not member_name:
            continue
        # Alt names
        if name in ALT_MEMBER_NAMES and ALT_MEMBER_NAMES[name] == member.name:
            return member
        if not member_name or not name:
            continue
        # Full name
        if name == member_name:
            return member
        # First part or last part
        if member_name.startswith(name) or member_name.endswith(name):
            return member
        # Without spaces
        if member_name.replace(' ', '') == name.replace(' ', ''):
            return member
    return None

def _parse_comic_title_parts(comic_title, version):
    for separator in PARTS_SEPARATORS_PER_VERSION[version]:
        parts = comic_title.split(separator)
        if len(parts) > 1:
            return parts[0].strip(), parts[1].strip()
    print '  ! Warning: Couldn\'t parse data from title. Using full title as name with no data.'
    return '', comic_title

def parse_comic_title(all_members, comic_title, version):
    data = {}
    data_string, comic_name = _parse_comic_title_parts(comic_title, version)
    for separator in CHARACTER_OR_BAND_SEPARATORS_PER_VERSION[version]:
        data_string = data_string.replace(separator, '&')
    for band_or_member in data_string.split('&'):
        if not band_or_member:
            continue
        # Ignore #1, #2 at the end of the tags
        for i in range(9):
            if u'#{}'.format(i) in band_or_member:
                band_or_member = band_or_member.replace(u'#{}'.format(i), '')
        band_or_member = band_or_member.strip()
        if not band_or_member:
            continue
        # Band name
        if band_or_member in models.Song.BAND_CHOICES: # Has more bands than Member.BAND_CHOICES
            data['band'] = models.Song.get_i('band', band_or_member)
            continue
        # Band alt names:
        if band_or_member in BAND_ALT_NAMES:
            data['band'] = models.Song.get_i('band', BAND_ALT_NAMES[band_or_member])
            continue
        # Member name (can be full name of first name)
        member = find_member_from_name_or_partial_name(all_members, band_or_member, version)
        if member:
            if 'members' not in data:
                data['members'] = []
            data['members'].append(member)
            continue
        print '  ! Warning: Couldn\'t parse any data for prefix part', band_or_member
    return data, comic_name.replace(u'「', '').replace(u'」', '')

def find_possible_matching_comics_from_data(data, comics_bundles, version):
    possible_matches = []
    for bundle, comic in comics_bundles.items():
        if (not comic.original_urls.get(version, None) # Can't be a match if already has image
            and comic.parsed_data == data):
            possible_matches.append((bundle, comic))
    return possible_matches

def find_existing_comic_by_id(comics_bundles, id):
    for bundle, comic in comics_bundles.items():
        if comic.id == id:
            return bundle, comic
    return None, None

def download_image_file(url):
    if not url:
        return None
    img_temp = NamedTemporaryFile(delete=True)
    r = requests.get(url)
    # Read the streamed image in sections
    for block in r.iter_content(1024 * 8):
        # If no more file then stop
        if not block:
            break
        # Write image block to temporary file
        img_temp.write(block)
    img_temp.flush()
    return ImageFile(img_temp)

def resize_image_from_data(data, filename, width=200, height=200):
    _, extension = os.path.splitext(filename)
    extension = extension.lower()
    image = Image.open(cStringIO.StringIO(data))
    image = image.resize((int(width), int(height)))
    output = io.BytesIO()
    image.save(output, format={
        'png': 'PNG',
        'jpg': 'JPEG',
        'jpeg': 'JPEG',
        'gif': 'GIF',
    }.get(extension.lower(), 'PNG'))
    return dataToImageFile(output.getvalue())

def import_comics(args):
    comics_bundles = {}
    comics_in_db = models.Asset.objects.filter(i_type=models.Asset.get_i('type', 'comic'), value=1)
    all_members = models.Member.objects.all()
    owner = get_owner()
    added_comics = 0
    updated_comics = 0

    for version, version_details in [(v, vv) for v, vv in models.Account.VERSIONS.items() if v == 'KR'] + [(v, vv) for v, vv in models.Account.VERSIONS.items() if v != 'KR']:
        language = models.VERSIONS_TO_LANGUAGES[version]

        print 'Downloading list of comics for', unicode(version_details['translation']), '...'
        filename = u'comics_{}.json'.format(version.lower())
        if 'local' in args:
            f = open(filename, 'r')
            result = json.loads(f.read())
        else:
            r = requests.get(u'https://api.bangdream.ga/v1/{}/sfc'.format(version.lower()))
            result = r.json()
            filed = open(filename, 'w')
            json.dump(result, filed)
            filed.close()

        print '  Found', result['totalCount'], 'comics for', unicode(version_details['translation']), '.'

        for comic in result['data']:
            print '    Adding', comic['title']
            data, comic_name = parse_comic_title(all_members, comic['title'], version)
            print '     ', comic_name, data
            comic_bundle = comic['assetBundleName']
            image_url = u'https://bangdream.ga{}'.format(comic['assetAddress'])
            image_field_name = u'{prefix}image'.format(prefix=version_details['prefix'])
            existing_comic = None
            existing_comic = find_existing_comic_by_name(comics_in_db, language, comic_name)
            if not existing_comic and comic_bundle in comics_bundles and comics_bundles[comic_bundle]:
                existing_comic = comics_bundles[comic_bundle]
                # If the data doesn't match, it's likely not the same comic so it will be re-added as a separate one
                # No way to detect which one is the right one, so it prints a warning and gives potential matches
                # And users can pick a match
                if existing_comic.parsed_data != data:
                    existing_comic = None
                    comic_bundle += '-special'
                    print '      !! Warning: Different data found from previously added with same bundle'
                    print '      Image URL:', image_url
                    accepted_match = False
                    possible_matches = find_possible_matching_comics_from_data(data, comics_bundles, version)
                    if possible_matches:
                        print 'Possible matches:'
                        for matching_bundle, matching_comic in possible_matches:
                            print '        ', matching_comic.id, matching_comic.original_urls
                            # Prompt to check and accept match
                            answer = None
                            try:
                                while answer not in ['yes', 'no']:
                                    answer = input('        Use this match? (yes/no) ')
                                    if answer == 'yes':
                                        existing_comic = matching_comic
                                        comic_bundle = matching_bundle
                                        accepted_match = True
                            except KeyboardInterrupt:
                                print ''
                                print 'Operation cancelled.'
                                sys.exit(1)
                            if accepted_match:
                                break
                    else:
                        print '      No match found, adding by itself.'
                    if not accepted_match:
                        try:
                            answer = None
                            while not answer:
                                answer = input('        Select a match manually? (Asset id or "no")')
                                if answer and answer != 'no':
                                    found_bundle, found_comic = find_existing_comic_by_id(comics_bundles, int(answer))
                                    if not found_comic:
                                        print '        Not found.'
                                        answer = None
                                    else:
                                        existing_comic = found_comic
                                        comic_bundle = found_bundle
                                        accepted_match = True
                        except KeyboardInterrupt:
                            print ''
                            print 'Operation cancelled.'
                            sys.exit(1)

            should_download_image = True
            if (existing_comic
                and getattr(existing_comic, image_field_name, None)
                and 'redownload' not in args):
                comic = existing_comic
                for k, v in data.items():
                    if k == 'members':
                        for member in v:
                            if member not in comic.members.all():
                                comic.members.add(member)
                    else:
                        setattr(comic, k, v)
                should_download_image = False
                print '     ', comic_name, 'already exists and has image in this version.'
            else:
                if existing_comic:
                    comic = existing_comic
                    had_already = bool(getattr(existing_comic, image_field_name, None))
                    if k == 'members':
                        for member in v:
                            if member not in comic.members.all():
                                comic.members.add(member)
                    else:
                        setattr(comic, k, v)
                    if language == 'en':
                        comic.name = comic_name
                    else:
                        comic.add_d('names', language, comic_name)
                    if had_already:
                        print '      Update image...'
                        updated_comics += 1
                    else:
                        print '      Add image...'
                        added_comics += 1
                else:
                    print '      Create asset...'
                    data = {
                        'owner': owner,
                        'i_type': models.Asset.get_i('type', 'comic'),
                        'name': comic_name if language == 'en' else None,
                        'value': 1,
                    }
                    comic = models.Asset.objects.create(**data)
                    print '      Done.'
                    if language != 'en':
                        comic.add_d('names', language, comic_name)
                    print '      Add image...'
                    added_comics += 1

            comic.parsed_data = data
            if not hasattr(comic, 'original_urls'):
                comic.original_urls = {}
            comic.original_urls[version] = image_url
            comics_bundles[comic_bundle] = comic

            if should_download_image:
                if 'nodownload' not in args:
                    image = download_image_file(image_url)
                    filename = image.name
                    if not image:
                        print '!! Error while downloading image for comic', comic_name
                        continue
                    if version in VERSIONS_NEED_RESIZE:
                        adjusted_width = image.height * 600 / 436
                        print u'        Resize image from {}x{} to {}x{}...'.format(
                            image.width, image.height,
                            adjusted_width, image.height,
                        )
                        image = resize_image_from_data(image.read(), filename, width=adjusted_width, height=image.height)
                    image.name = models.Asset._meta.get_field('image').upload_to(comic, filename)
                    setattr(comic, image_field_name, image)
                    print '        Done.'

                print '      Comic:', comic.http_item_url
                print '      Done.'

            comic.save()
            # -- End of for per comic
        # -- End of for per version

        print 'End of', unicode(version_details['translation']), '.'

    print added_comics, 'comics have been added.'
    if 'redownload' in args or updated_comics:
        print updated_comics, 'comics have been updated.'

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        import_comics(args)
