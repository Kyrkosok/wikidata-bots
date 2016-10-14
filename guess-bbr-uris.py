import wikibot, re
from ksamsok import KSamsok

#
# This bot is used to fix broken BBR links by guessing
# the URIs and check if the new one verifies in KSamsok-py
#
# user-config.py:
# family = 'wikidata'
# mylang = 'wikidata'
#

sparql = 'SELECT ?item  ?c WHERE { ?item wdt:P1260 ?c . FILTER(CONTAINS(?c, "bbr/")) }'
culturalSerach = KSamsok('test')

bot = wikibot.Bot(True)
generator = wikibot.Generator.newSparQLGenerator(bot, sparql)
for p in generator:
    item = wikibot.Item(p)
    uri = item.item.claims['P1260'][0].getTarget()
    if not culturalSerach.formatUri(uri, 'raw', True):
        # the uri was not valid
        # create other bbr links
        uri_a = re.sub('bbr', 'bbra', uri)
        uri_b = re.sub('bbr', 'bbrb', uri)
        uri_m = re.sub('bbr', 'bbrm', uri)

        if culturalSerach.formatUri(uri_a, 'raw', True):
            print('bbra')
            target = uri_a
            item.item.claims['P1260'][0].changeTarget(target)
        elif culturalSerach.formatUri(uri_b, 'raw', True):
            print('bbrb')
            target = uri_b
            item.item.claims['P1260'][0].changeTarget(target)
        elif culturalSerach.formatUri(uri_m, 'raw', True):
            print('bbrm')
            target = uri_m
            item.item.claims['P1260'][0].changeTarget(target)
        else:
            print('failed to fix: ' + str(item.item))