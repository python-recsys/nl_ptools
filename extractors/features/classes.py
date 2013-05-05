#-*-coding: utf-8 -*-
from extractors.features.base import TfIdfVectorizer
from extractors.features.base import CountVectorizer
from extractors.features.base import BooleanVectorizer
from extractors.utils import remove_stopwords
import numpy as np

IDF_DEFAULT = 1.5


class CustomTfIdfVectorizer(TfIdfVectorizer):
    """
        TfIDFFeatureVectorizers must extend this class
         for vectorization behaviour
    """
    def __init__(self, tokenizer):
        self._tokenizer = tokenizer

    def __iter__(self):
        for index, item_id in enumerate(self.item_ids()):
            yield item_id, self[item_id]

    def idf(self, term):
        if not term in self.vocabulary:
            return IDF_DEFAULT

        doc_count = float(len(self.index))
        idx_token = self.vocabulary.index(term)
        docs = (self._tokens[idx_token])

        return np.log(1 + doc_count) / (1 + len(docs))

    def transform(self, sample, corpus=None, tokenizer=None):
        if self.index is None:
            self.build_vector(corpus, tokenizer)

        if tokenizer is None:
            tokenizer = self._tokenizer

        tokens = tokenizer.tokenize(sample)
        tokens = remove_stopwords([token.lower()
                    for token in tokens], 'all')

        tfidf = {}
        tokens_set = set(tokens)
        for word in tokens_set:
            if word in self.vocabulary:
                mytf = float(tokens.count(word)) / len(tokens_set)
                myidf = self.idf(word)
                idx_token = self.vocabulary.index(token)
                tfidf[idx_token] = mytf * myidf

        output = {'text': sample, 'tokens': tokens,
            'tfidf': self.normalize(tfidf) if  tfidf else {}}
        return output

    def add_input(self, sample, corpus=None, tokenizer=None):
        if self.index is None:
            id_database = len(corpus) + 1
            corpus.update({id_database: sample})
            return self.build_vector(corpus, tokenizer)
        else:
            id_database = len(self._item_ids) + 1
            if tokenizer is None:
                tokenizer = self._tokenizer

            tokens = tokenizer.tokenize(sample)
            tokens = remove_stopwords([token.lower()
                    for token in tokens], 'all')
            self.index[id_database] = {'text': sample, \
                'tokens': tokens}
            self.index[id_database].setdefault('tfidf', {})

            tokens = self.index[id_database]['tokens']
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary.append(token)
                idx_token = self.vocabulary.index(token)
                self.index[id_database]['tfidf'].setdefault(idx_token, 0)
                self.index[id_database]['tfidf'][idx_token] += 1

            tfidfs = self.index[id_database]['tfidf']

            if len(tokens) > 0:
                for token, freq in tfidfs.iteritems():
                    self._tokens.setdefault(token, []).append(
                                (id_database, float(freq) / len(tokens)))
            tokens_set = set(tokens)
            ids_databases = []
            for word in tokens_set:
                idf = self.idf(word)
                idx_token = self.vocabulary.index(word)
                docs = (self._tokens[idx_token])
                for id_d, tf in docs:
                    tfidf = tf * idf
                    if tfidf > 0:
                        self.index[id_d]['tfidf'][token] = tfidf
                        ids_databases.append(id_d)

            for id_database in ids_databases:
                self.index[id_database]['tfidf'] = \
                    self.normalize(self.index[id_database]['tfidf'])

            self._item_ids = self.index.keys()
            return self.index, self.vocabulary

    def build_vector(self, corpus, tokenizer=None):
        if tokenizer is None:
            tokenizer = self._tokenizer

        self._item_ids = []
        self.vocabulary = []
        self.index = {}
        self._tokens = {}
        for i, id_database in enumerate(corpus):
            tokens = tokenizer.tokenize(corpus[id_database])
            tokens = remove_stopwords([token.lower()
                    for token in tokens], 'all')
            self.index[id_database] = {'text': corpus[id_database], \
                'tokens': tokens}
            self.index[id_database].setdefault('tfidf', {})

            tokens = self.index[id_database]['tokens']
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary.append(token)
                idx_token = self.vocabulary.index(token)
                self.index[id_database]['tfidf'].setdefault(idx_token, 0)
                self.index[id_database]['tfidf'][idx_token] += 1

            tfidfs = self.index[id_database]['tfidf']

            if len(tokens) > 0:
                for token, freq in tfidfs.iteritems():
                    self._tokens.setdefault(token, []).append(
                                (id_database, float(freq) / len(tokens)))

        doc_count = float(len(corpus))
        for token, docs in self._tokens.iteritems():
            idf = np.log(doc_count / len(docs))
            for id_d, tf in docs:
                tfidf = tf * idf
                if tfidf > 0:
                    self.index[id_d]['tfidf'][token] = tfidf
        for id_database in self.index:
            self.index[id_database]['tfidf'] = \
                    self.normalize(self.index[id_database]['tfidf'])

        self._item_ids = self.index.keys()

        return self.index, self.vocabulary

    def normalize(self, features):
        norm = 1.0 / np.sqrt(sum(i ** 2 for i in features.itervalues()))
        for k, v in features.iteritems():
            features[k] = v * norm
        return features


class CustomCountVectorizer(CountVectorizer):
    """
        FrequencyCountVectorizers must extend this class
         for vectorization behaviour
    """
    def __init__(self, tokenizer):
        self._tokenizer = tokenizer

    def __iter__(self):
        for index, item_id in enumerate(self.item_ids()):
            yield item_id, self[item_id]

    def add_input(self, sample, corpus=None, tokenizer=None):
        if self.index is None:
            id_database = len(corpus) + 1
            corpus.update({id_database: sample})
            return self.build_vector(corpus, tokenizer)
        else:
            id_database = len(self._item_ids) + 1
            if tokenizer is None:
                tokenizer = self._tokenizer

            tokens = tokenizer.tokenize(sample)
            tokens = remove_stopwords([token.lower()
                    for token in tokens], 'all')
            self.index[id_database] = {'text': sample, \
                'tokens': tokens}
            self.index[id_database].setdefault('tf', {})

            tokens = self.index[id_database]['tokens']
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary.append(token)
                idx_token = self.vocabulary.index(token)
                self.index[id_database]['tf'].setdefault(idx_token, 0)
                self.index[id_database]['tf'][idx_token] += 1

            self._item_ids = self.index.keys()
            return self.index, self.vocabulary

    def build_vector(self, corpus, tokenizer=None):
        if tokenizer is None:
            tokenizer = self._tokenizer

        self.vocabulary = []
        self.index = {}
        for i, id_database in enumerate(corpus):
            tokens = tokenizer.tokenize(corpus[id_database])
            tokens = remove_stopwords([token.lower()
                    for token in tokens], 'all')
            self.index[id_database] = {'text': corpus[id_database], \
                'tokens': tokens}
            self.index[id_database].setdefault('tf', {})

            tokens = self.index[id_database]['tokens']
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary.append(token)
                idx_token = self.vocabulary.index(token)
                self.index[id_database]['tf'].setdefault(idx_token, 0)
                self.index[id_database]['tf'][idx_token] += 1

        self._item_ids = self.index.keys()

        return self.index, self.vocabulary

    def transform(self, sample, corpus=None, tokenizer=None):
        if self.index is None:
            self.build_vector(corpus, tokenizer)

        if tokenizer is None:
            tokenizer = self._tokenizer

        tokens = tokenizer.tokenize(sample)
        tokens = remove_stopwords([token.lower()
                    for token in tokens], 'all')

        output = {'text': sample, 'tokens': tokens,
            'tf': dict((self.vocabulary.index(token), tokens.count(token))
                 for token in list(set(tokens)) if token in self.vocabulary)}

        return output


class CustomBooleanVectorizer(BooleanVectorizer):
    """
        BooleanVectorizers must extend this class for vectorization behaviour
    """
    def __init__(self, tokenizer):
        self._tokenizer = tokenizer

    def __iter__(self):
        for index, item_id in enumerate(self.item_ids()):
            yield item_id, self[item_id]

    def add_input(self, sample, corpus=None, tokenizer=None):
        if self.index is None:
            id_database = len(corpus) + 1
            corpus.update({id_database: sample})
            return self.build_vector(corpus, tokenizer)
        else:
            id_database = len(self._item_ids) + 1
            if tokenizer is None:
                tokenizer = self._tokenizer

            tokens = tokenizer.tokenize(sample)
            tokens = remove_stopwords([token.lower()
                    for token in tokens], 'all')
            self.index[id_database] = {'text': sample, \
                'tokens': tokens}
            self.index[id_database].setdefault('boolean', {})

            tokens = self.index[id_database]['tokens']
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary.append(token)
                idx_token = self.vocabulary.index(token)
                self.index[id_database]['boolean'].setdefault(idx_token, 0)
                self.index[id_database]['boolean'][idx_token] = True

            self._item_ids = self.index.keys()
            return self.index, self.vocabulary

    def build_vector(self, corpus, tokenizer=None):
        if tokenizer is None:
            tokenizer = self._tokenizer

        self.vocabulary = []
        self.index = {}
        for i, id_database in enumerate(corpus):
            tokens = tokenizer.tokenize(corpus[id_database])
            tokens = remove_stopwords([token.lower()
                    for token in tokens], 'all')
            self.index[id_database] = {'text': corpus[id_database], \
                'tokens': tokens}
            self.index[id_database].setdefault('boolean', {})

            tokens = self.index[id_database]['tokens']
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary.append(token)
                idx_token = self.vocabulary.index(token)
                self.index[id_database]['boolean'].setdefault(idx_token, 0)
                self.index[id_database]['boolean'][idx_token] = True

        self._item_ids = self.index.keys()

        return self.index, self.vocabulary

    def transform(self, sample, corpus=None, tokenizer=None):
        if self.index is None:
            self.build_vector(corpus, tokenizer)

        if tokenizer is None:
            tokenizer = self._tokenizer

        tokens = tokenizer.tokenize(sample)
        tokens = remove_stopwords([token.lower()
                    for token in tokens], 'all')

        output = {'text': sample, 'tokens': tokens,
            'tf': dict((self.vocabulary.index(token), True)
                 for token in list(set(tokens)) if token in self.vocabulary)}

        return output
