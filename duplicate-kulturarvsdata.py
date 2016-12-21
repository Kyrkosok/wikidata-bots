import wikibot, re

#
# This bot is used to detect duplicate P1260(kulturarvsdata) statements
#
# user-config.py:
# family = 'wikidata'
# mylang = 'wikidata'
#

bot = wikibot.Bot()
sparql = 'SELECT ?item ?value WHERE { ?item wdt:P1260 ?value . }'
generator = wikibot.Generator.newSparQLGenerator(bot, sparql)

for item in generator:
    item.get()
    if item.claims:
        if 'P1260' in item.claims:
            claims = []
            for claim in item.claims['P1260']:
                target = claim.getTarget()
                claims.append(target)
            if (len(claims) != len(set(claims))):
                print(item)
