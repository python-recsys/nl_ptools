#-*- coding: utf-8 -*-
import sys
from extractors.features import CustomTfIdfVectorizer, CustomCountVectorizer
from extractors.features import CustomBooleanVectorizer
from extractors.tokenizers import BaseTokenizer
from extractors.keywords import PMIKeyExtractor
from extractors.tagging import Tagger
from extractors.keywords import TaggerKeyExtractor
from extractors.language import NaiveLangDetector
from extractors.keywords import GroupKeyExtractor

naive = NaiveLangDetector()
base_tokenizer = BaseTokenizer()
tagger = Tagger(base_tokenizer, naive)

key_extractor = TaggerKeyExtractor(None, tagger)
print key_extractor.keywords(u'Paulo Maluf é um canalha!')

nltk_keyword = PMIKeyExtractor()
print nltk_keyword.keywords(u'Coca-Cola sempre me surpreendeu com os melhores refrigerantes!')

group_extractor = GroupKeyExtractor(key_extractor, nltk_keyword)
print group_extractor.keywords([u'Paulo Maluf é um canalha!', u'Paulo Maluf seu safado!'])
