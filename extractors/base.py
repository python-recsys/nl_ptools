#-*- coding:utf-8 -*-


class BaseExtractor(object):
    """
        Extractors must extend this class for extraction behaviour.
    """

    def extract(self, query):
        raise NotImplementedError("Override this method" +
                "for extraction support")


class BaseFeatureVectorizer(object):
    """
        FeatureVectorizers must extend this class for vectorization behaviour
    """
    def build_vector(self, corpus):
        raise NotImplementedError("Override this method" +
            "for vectorization support")


class BaseDetector(object):
    """
        Detectors must extend this class for language detection.
    """
    def language(self, query):
        raise NotImplementedError("Override this method" +
                "for detection support")



class BaseKeywordExtractor(object):
    """
        Extractors must extend this class for keyword extraction.
    """
    def keywords(self, query):
        raise NotImplementedError("Override this method" +
                "for keywords extraction support")


class BaseTagger(object):
    """
        Taggers must extend this class for tagging.
    """
    def tag(self, query):
        raise NotImplementedError("Override this method" +
                "for tagging support")


class BaseChunker(object):
    """
        Chunckers must extend this class for Noun phrase chuncking.
    """
    def entities(self, query):
        raise NotImplementedError("Override this method" +
                "for Noun phrase chuncking support")
