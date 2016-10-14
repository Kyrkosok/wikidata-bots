import wikibot, re

#
# This bot is used to make sure P1260(kulturarvsdata) statements
# points to the RDF(raw) URI instead of the HTMl one.
#
# user-config.py:
# family = 'wikidata'
# mylang = 'wikidata'
#

bot = wikibot.Bot()
sparql = 'SELECT ?item ?value WHERE { ?item wdt:P1260 ?value FILTER(regex(str(?value), "/html/")) }'
generator = wikibot.Generator.newSparQLGenerator(bot, sparql)

for item in generator:
    item.get()
    if item.claims:
        if 'P1260' in item.claims:
            for claim in item.claims['P1260']:
                target = claim.getTarget()
                target = re.sub('/html', '', target)
                claim.changeTarget(target)