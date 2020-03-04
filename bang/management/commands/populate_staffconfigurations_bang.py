# -*- coding: utf-8 -*-
import json
from django.core.management.base import BaseCommand
from magi.management.commands.populate_staffconfigurations import create
from magi import models as magi_models

class Command(BaseCommand):
    def handle(self, *args, **options):
        create({
            'key': 'christmas_theme_cards',
            'verbose_key': 'Christmas theme: which cards show up on the homepage?',
            'value': '786,787,788,789,790,1058,1059,1060,1061,1307,1308,1309,1310,1311',
        })
        create({
            'key': 'christmas_theme_backgrounds',
            'verbose_key': 'Christmas theme: which backgrounds show up on the homepage?',
            'value': '1204,818,817,838',
        })
        create({
            'key': 'christmas_theme_arts',
            'verbose_key': 'Christmas theme: extra images that show up on the homepage',
            'is_long': True,
            'value': json.dumps([
                {
                    'info': 'Centered on Rimi/Saaya',
                    'url': 'https://i.bandori.party/u/asset/fDmheSChristmas-no-Uta-Christmas-Song-jxAEmQ.jpg',
                    'side': 'left',
                    'position': { 'size': '130%', 'x': '30%', 'y': '20%' },
                },
                {
                    'info': 'Centered on Kasumi',
                    'url': 'https://i.bandori.party/u/asset/fDmheSChristmas-no-Uta-Christmas-Song-jxAEmQ.jpg',
                    'side': 'left',
                    'position': { 'size': '160%', 'x': '100%', 'y': '10%' },
                },
                {
                    'info': 'Centered on Arisa/Tae',
                    'url': 'https://i.bandori.party/u/asset/fDmheSChristmas-no-Uta-Christmas-Song-jxAEmQ.jpg',
                    'side': 'right',
                    'position': { 'size': '120%', 'x': '88%', 'y': '15%' },
                },
                {
                    'info': 'Centered on Kanon/Misaki',
                    'url': 'https://i.bandori.party/u/asset/i9bIUCHello-Happy-Christmas-89fB8F.jpg',
                    'side': 'left',
                    'position': { 'size': '150%', 'x': '118%', 'y': '15%' },
                },
                {
                    'info': 'Centered on Kokoro/Kaoru',
                    'url': 'https://i.bandori.party/u/asset/i9bIUCHello-Happy-Christmas-89fB8F.jpg',
                    'side': 'left',
                    'position': { 'size': '140%', 'x': '15%', 'y': '0%' },
                },
                {
                    'info': 'Centered on Hagumi',
                    'url': 'https://i.bandori.party/u/asset/i9bIUCHello-Happy-Christmas-89fB8F.jpg',
                    'side': 'right',
                    'position': { 'size': '160%', 'x': '100%', 'y': '0%' },
                },
                {
                    'info': 'Kasumi/Eve/Kanon repeated background',
                    'url': 'https://i.bandori.party/u/asset/pXRYpiOfficial-art-Merry-Christmas-Twn1PS.jpg',
                    'position': { 'size': '50%', 'x': '100%', 'y': '50%' },
                },
            ], indent=4, sort_keys=True),
        })
