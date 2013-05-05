#-*- coding: utf-8 -*-
import re
from stopwords import STOPWORDS

d = {192: u'A', 193: u'A', 194: u'A', 195: u'A', 196: u'A', 197: u'A',
     199: u'C', 200: u'E', 201: u'E', 202: u'E', 203: u'E', 204: u'I',
     205: u'I', 206: u'I', 207: u'I', 209: u'N', 210: u'O', 211: u'O',
     212: u'O', 213: u'O', 214: u'O', 216: u'O', 217: u'U', 218: u'U',
     219: u'U', 220: u'U', 221: u'Y', 224: u'a', 225: u'a', 226: u'a',
     227: u'a', 228: u'a', 229: u'a', 231: u'c', 232: u'e', 233: u'e',
     234: u'e', 235: u'e', 236: u'i', 237: u'i', 238: u'i', 239: u'i',
     241: u'n', 242: u'o', 243: u'o', 244: u'o', 245: u'o', 246: u'o',
     248: u'o', 249: u'u', 250: u'u', 251: u'u', 252: u'u', 253: u'y',
     255: u'y'}

NEGATION_TOKEN = 'NOT'
NEGATION_REGEX = re.compile(r'no{1,}t|no{1,}|na{1,}o{1,}|n\xe3{1,}o{1,}', re.U & re.IGNORECASE)

def asciize(string_com_acentos):
    return string_com_acentos.translate(d)

def rem_acentuacao(str):
    from unicodedata import normalize
    return normalize('NFKD', str.decode('utf-8')).encode('ASCII', 'ignore')

def remove_stopwords(tokens):
    tokens_stp = [token for token in tokens if token not in STOPWORDS]
    return tokens_stp

def ngram(seq, n):
    ngrams = [seq[i:i + n] for i in range(1 + len(seq) - n)]
    return [ngram  for ngram in ngrams]

def identify_negation(text):
    return NEGATION_REGEX.findall(text.lower())

def negation2token(tokens, neg_words):
    for word in neg_words:
        for idx in range(len(tokens)):
            if tokens[idx].lower() == word.lower():
                tokens[idx] = NEGATION_TOKEN
	return tokens

#http://jaganadhg.freeflux.net/blog/archive/2009/07/15/finding-bigrams-with-nltk.html