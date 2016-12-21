import wikibot, re
from ksamsok import KSamsok

#
# This bot is used to detect broken/invalid kulturarvsdata statements
# THIS BOT MAKES THOUSANDS OF HTTP CALLS TO THE Swedish National Heritage Board
# BE NICE.
#
# user-config.py:
# family = 'wikidata'
# mylang = 'wikidata'
#

bot = wikibot.Bot()
soch = KSamsok('test')
sparql = 'SELECT ?item ?value WHERE { ?item wdt:P1260 ?value . }'
generator = wikibot.Generator.newSparQLGenerator(bot, sparql)

for item in generator:
    item.get()
    if item.claims:
        if 'P1260' in item.claims:
            claims = []
            for claim in item.claims['P1260']:
                target = claim.getTarget()
                if not soch.formatUri(target, 'raw', True):
                    print(item)
