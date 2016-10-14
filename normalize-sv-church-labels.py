import wikibot, re

#
# This bot is used to normaize swedish church labels
# by removing the appended location, which where
# imported from the swedish Wikipedia title.
#
# user-config.py:
# family = 'wikidata'
# mylang = 'wikidata'
#

sparql = 'SELECT ?item  ?label (LANG(?label) AS ?lang) WHERE { ?item wdt:P31 wd:Q16970 . ?item wdt:P17 wd:Q34; rdfs:label ?label . FILTER(LANG(?label) IN ("sv")) . FILTER(CONTAINS(?label, ", ")) . }'

bot = wikibot.Bot(True)
generator = wikibot.Generator.newSparQLGenerator(bot, sparql)
for i in generator:
    item = wikibot.Item(i)
    label = item.getLabel('sv')
    label = re.sub(', .+', '', label)
    
    item.editLabel('sv', label, 'normalizing imported label', True)