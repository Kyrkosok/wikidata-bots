import sys, pywikibot, mwparserfromhell, re, requests
from pywikibot import pagegenerators
class Bot:
    def __init__(self, notebook = False):
        if notebook:
            self.site = pywikibot.Site()
        else:
            pywikibot.handle_args(sys.argv[1:])
            self.site = pywikibot.Site()

class Generator:
    @staticmethod
    def newTemplateGenerator(bot, template):
        transclusionPage = pywikibot.Page(pywikibot.Link(template, defaultNamespace = 10, source = bot.site))        
        return pagegenerators.ReferringPageGenerator(transclusionPage, onlyTemplateInclusion = True)
    
    @staticmethod
    def newSparQLGenerator(bot, sparql):
        return pagegenerators.WikidataSPARQLPageGenerator(sparql, site = bot.site)
    
    @staticmethod
    def newCategoryGenerator(bot, category):
        cat = pywikibot.Category(bot.site, category)
        return pagegenerators.CategorizedPageGenerator(cat)
        

class Page:
    def __init__(self, page):
        self.page = page
        self.wikitext = mwparserfromhell.parse(page.text)

    def getTemplateProperty(self, template, property):
        for t in self.wikitext.filter_templates():
            if t.name.matches(template):
                p = re.sub('^\s+', '', str(t.get(property).value))
                p = re.sub('$\n+', '', p)
                return p
        return False

    def addPropertyToTemplate(self, template, property, value, msg):
        for t in self.wikitext.filter_templates():
            try:
                if t.name.matches(template):
                    t.add(property, value)
                    self.page = self.wikitext.str()
                    print(self.wikitext.str())
                    self.page.save(msg)
            except:
                return    

    def getWikidataItem(self):
        try:
            i = pywikibot.ItemPage.fromPage(self.page)
            return i
        except pywikibot.NoPage:
            return False

    def replaceString(self, old, new, msg):
        self.page.text = re.sub(old, new, self.page.text)
        self.page.save(msg)

class Item():
    def __init__(self, item, bot = None):
        if isinstance(item, str):
            self.item = pywikibot.ItemPage(bot.site.data_repository(), item)
        else:
            self.item = item

        self.item.get()
    
    def getLabel(self, language):       
        if language in self.item.labels:
            return self.item.labels[language]
        
        return False
    
    def editLabel(self, language, label, comment, hard = False):
        if hard:
            self.item.editLabels(labels = {language: label}, summary = comment)
        else:
            if not self.getLabel(language):
                self.item.editLabels(labels = {language: label}, summary = comment)
                
    def getDescription(self, language):
        if language in self.item.descriptions:
            return self.item.descriptions[language]
        
        return False
    
    def editDescription(self, language, description, comment, hard = False):
        if hard:
            self.item.editDescriptions(descriptions = {language: label}, summary = comment)
        else:
            if not self.getDescription(language):
                self.item.editDescriptions(descriptions = {language: label}, summary = comment)
    
    def getClaims(self, property):
        if (self.item.claims):
            if property in self.item.claims:
                return self.item.claims[property]
            else:
                return False
        else:
            return False

def returns404(url):    
    r = requests.get(url)
    if r.status_code == 404:
        return True
    else:
        return False
    