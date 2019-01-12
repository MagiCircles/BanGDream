from django.core.management.base import BaseCommand, CommandError
from magi.utils import LANGUAGES_DICT
from magi.management.commands.populate_staffconfigurations import create

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):


        # Template
        #
        # create({
        #     'key': '',
        #     'verbose_key': '',
        #     'value': '',
        #     'is_markdown': True,
        #     'is_long': True,
        #     'is_boolean': True,
        # })

        # Skill

        for language in LANGUAGES_DICT.keys():
            create({
                'key': 'skill_types_translations',
                'verbose_key': 'Skill: Translations for types',
                'i_language': language,
                'value': u'Score Up, Life Recovery, Perfect Lock, Life Guard' if language is 'en' else None,
            })
        create({
            'key': 'skill_types',
            'verbose_key': 'Skill: Keys for types',
            'value': 'score, heal, accuracy, guard',
        })
        create({
            'key': 'skill_icons',
            'verbose_key': 'Skill: Icons for types',
            'value': 'scoreup, healer, perfectlock, fingers',
        })
