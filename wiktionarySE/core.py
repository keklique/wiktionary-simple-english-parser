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


    def fetch(self, word):
        response = self.session.get(self.url.format(word))
        self.soup = BeautifulSoup(response.text.replace('>\n<', '><'), 'html.parser')
        self.current_word = word
        self.get_body_content()
        self.remove_editsections()
        print(self.soup)
        # return self.get_word_data()


w = WiktionarySE()
w.fetch("index")