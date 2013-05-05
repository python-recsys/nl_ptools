from extractors.base import BaseKeywordExtractor
from extractors.lib import AlchemyAPI
from extractors.html_extractors import DiffbotExtractor
from django.utils import simplejson
from nltk.collocations import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from nltk import wordpunct_tokenize, FreqDist
from nltk import corpus


class AlchemyKeyExtractor(BaseKeywordExtractor):
    def __init__(self, api_key):
        self.api_key = api_key
        self.alchemy_api = AlchemyAPI()
        self.alchemy_api.setAPIKey(self.api_key)

    def _fetch_url(self, url):
        try:
            result = self.alchemy_api.URLGetRankedKeywords(url)
        except Exception, e:
            return {'errorCode': 404, 'errors': str(e)}

        return result

    def _fetch_text(self, text):
        try:
            result = self.alchemy_api.TextGetRankedKeywords(text)
        except Exception, e:
            return {'errorCode': 404, 'errors': str(e)}

        return result

    def keywords(self, query):
        if query.startswith('www') or query.startswith('http'):
            result = self._fetch_url(query)

            json = simplejson.loads(result.decode('utf-8'))

            if 'errorCode' in json or json['status'] != 'OK':
                return json
            else:
                keywords = json['keywords']
            return {'response': {'language': json['language'],
                    'keywords': keywords, 'url': query}}

        else:
            result = self._fetch_text(query)

            json = simplejson.loads(result.decode('utf-8'))

            if 'errorCode' in json or json['status'] != 'OK':
                return json
            else:
                keywords = json['keywords']
            return {'response': {'language': json['language'],
                    'keywords': keywords, 'text': query}}


class TaggerKeyExtractor(BaseKeywordExtractor):

    def __init__(self, html_extractor=None, tagger=None):
        self.tagger = tagger
        self.html_extractor = html_extractor

    def _fetch_text(self, text):
        tags = self.tagger.tag(text)['response']['taggings'][0]
        keywords = [token.decode('utf-8') for token, tagging in tags \
                        if tagging.startswith('N')]
        return keywords

    def keywords(self, query):
        if query.startswith('www') or query.startswith('http'):
            text = self.html_extractor.extract(query)['response']['text']
            result = self._fetch_text(text)
            for r in result:
                print r
            keywords = result
            return {'response': {'language': '',
                    'keywords': keywords, 'text': query}}
        else:
            result = self._fetch_text(query)
            keywords = result
            keywords = FreqDist(w.lower() for w in keywords)
            return {'response': {'language': '',
                    'keywords': keywords.items(), 'text': query}}


class PMIKeyExtractor(BaseKeywordExtractor):

    def __init__(self, html_extractor=None, n_best = 2):
        self.html_extractor = html_extractor
        self.n_best = n_best

    def _fetch_text(self, text):
        bigram_measures = BigramAssocMeasures()
        tokens = wordpunct_tokenize(text)
        finder = BigramCollocationFinder.from_words(tokens)
        # only bigrams that appear 2+ times
        finder.apply_freq_filter(self.n_best)
        return finder.nbest(bigram_measures.pmi, 5)
        stopwords = corpus.stopwords.words('portuguese')
        #print stopwords
        #return FreqDist(w.lower() for w in tokens if w not in stopwords)

    def keywords(self, query):
        if query.startswith('www') or query.startswith('http'):
            text = self.html_extractor.extract(query)['response']['text']
            result = self._fetch_text(text)
            for r in result:
                print r
            keywords = result
            return {'response': {'language': '',
                    'keywords': keywords, 'text': query}}
        else:
            result = self._fetch_text(query)
            keywords = result
            print keywords
            keywords = FreqDist(u' '.join(w).lower() for w in keywords for idx in range(self.n_best))
            return {'response': {'language': '',
                    'keywords': keywords.items(), 'text': query}}


class GroupKeyExtractor(BaseKeywordExtractor):

    def __init__(self, key_extractor=None, bg_extractor=None):
        self.key_extractor = key_extractor
        self.bg_extractor = bg_extractor

    def keywords(self, query):
        final_text = u' '.join(query)

        resultKE = self.key_extractor._fetch_text(final_text)
        resultFE = self.bg_extractor._fetch_text(final_text)
        keywordsFE = [u' '.join(w).lower() for w in resultFE for idx in range(self.bg_extractor.n_best)]
        keywordsFE += resultKE

        keywords = FreqDist(w.lower() for w in keywordsFE)
        return {'response': {'language': '',
                    'keywords': keywords.items(), 'text': query}}


class NMFExtractor(BaseKeywordExtractor):

    def __init__(self, key_extractor=None, bg_extractor=None):
        self.n_features = 1000
        self.n_samples = 1000
        self.n_topics = 10
        self.n_top_words = 20

    def keywords(self):
        from sklearn.feature_extraction import text
        from sklearn import decomposition
        vectorizer = text.CountVectorizer(max_df=0.95, max_features=self.n_features)
        counts = vectorizer.fit_transform(dataset.data[:self.n_samples])
        tfidf = text.TfidfTransformer().fit_transform(counts)
        nmf = decomposition.NMF(n_components=self.n_topics).fit(tfidf)
        feature_names = vectorizer.get_feature_names()

        for topic_idx, topic in enumerate(nmf.components_):
            print "Topic #%d:" % topic_idx
            print " ".join([feature_names[i]
                    for i in topic.argsort()[:-self.n_top_words - 1:-1]])
