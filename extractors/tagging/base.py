#-*- coding: utf-8 -*-
from extractors.base import BaseTagger
import os
import pickle
from nltk.tag.hunpos import HunposTagger
from lib.Aelius import carrega, AnotaCorpus

PATH_MODEL = os.path.join(os.path.dirname(__file__), 'lib/aelius_data/AeliusBRUBT.pkl')

class Tagger(BaseTagger):

    def __init__(self, tokenizer, detector):
        self.tagger = AnotaCorpus
        self.tokenizer = tokenizer
        self.detector = detector

    def tag(self, query):
        b = carrega(PATH_MODEL)
        t = self.tagger.TokPort.tokenize(query)
        tagged = self.tagger.anota_sentencas([t], b, 'nltk')

        return {'response': {'taggings': tagged, 'text': query}}
