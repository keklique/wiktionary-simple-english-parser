import re, requests
from bs4 import BeautifulSoup
from copy import copy

PARTS_OF_SPEECH = [
    "noun", "verb", "adjective", "adverb", "determiner",
    "article", "preposition", "conjunction", "proper noun",
    "letter", "character", "phrase", "proverb", "idiom",
    "symbol", "syllable", "numeral", "initialism", "interjection",
    "definitions", "pronoun", "particle", "predicative", "participle",
    "suffix",
]

RELATIONS = [
    "synonyms", "antonyms", "hypernyms", "hyponyms",
    "meronyms", "holonyms", "troponyms", "related terms",
    "coordinate terms",
]

class WiktionarySE():
    def __init__(self):
        self.url = "https://simple.wiktionary.org/wiki/{}"
        self.soup = None
        self.session = requests.Session()
        self.session.mount("http://", requests.adapters.HTTPAdapter(max_retries = 2))
        self.session.mount("https://", requests.adapters.HTTPAdapter(max_retries = 2))
        self.PARTS_OF_SPEECH = copy(PARTS_OF_SPEECH)
        self.RELATIONS = copy(RELATIONS)
        self.INCLUDED_ITEMS = self.RELATIONS + self.PARTS_OF_SPEECH + ['etymology', 'pronunciation']

    def get_body_content(self):
        self.soup = self.soup.find("div",{"id":"bodyContent"})
        
    
    def remove_editsections(self):
        for editsection in self.soup.find_all("span", {'class': "mw-editsection"}):
            editsection.extract()

    def get_means(self):
        self.means = {}
        headers2 = self.soup.findAll("h2")
        for header2 in headers2:
            pos = header2.text.lower()
            if(pos =="contents"):
                continue
            temp_element = header2.find_next_sibling()
            c = 0
            while(True and c<10): 
                if(temp_element.name != 'ol' and temp_element.name != "h2" ):
                    temp_element = temp_element.find_next_sibling()
                    c+=1
                elif(temp_element.name == 'ol'):
                    mean_table = temp_element
                    uls = mean_table.find_all("ul")
                    for ul in uls:
                        ul.extract()
                    if(pos in PARTS_OF_SPEECH):
                        self.means[pos] = self.parse_definition_list(mean_table)
                    break
    
    def parse_definition_list(self,ol):
        definitions = []
        lis = ol.find_all("li")
        for li in lis:
            examples = []
            definition_tag = ""
            dds = li.find_all("dd")
            if(dds != []):
                for dd in dds:
                    examples.append(dd.text.strip())
                    dd.extract()
            tags = li.find_all("i")
            if(tags != []):
                for tag in tags:
                    try:
                        tag.find("span").text
                        definition_tag = tag.text.strip()
                        tag.extract()
                    except:
                        pass 
            expance_spans = li.find_all("span",{"class":"HQToggle"})
            if(expance_spans != []):
                for expance_span in expance_spans:
                    expance_span.extract()
            expance_spans = li.find_all("ul",{"class":"onyms-collapse"})
            if(expance_spans != []):
                for expance_span in expance_spans:
                    expance_span.extract()
            definition = li.text.replace("()","").strip()
            definitions.append({"definition":definition,"examples":examples,"tags":definition_tag})
        return definitions

        
            
    def fetch(self, word):
        response = self.session.get(self.url.format(word))
        self.soup = BeautifulSoup(response.text.replace('>\n<', '><'), 'html.parser')
        self.current_word = word
        self.get_body_content()
        self.remove_editsections()
        self.get_means()
        print(self.means)

w = WiktionarySE()
w.fetch("sniff")