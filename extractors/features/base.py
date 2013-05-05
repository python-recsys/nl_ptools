#-*-coding: utf-8 -*-

from extractors.base import BaseFeatureVectorizer


class TfIdfVectorizer(BaseFeatureVectorizer):
    """
        TfIDFFeatureVectorizers must extend this class
         for vectorization behaviour
    """
    def build_vector(self, corpus):
        raise NotImplementedError("Override this method" +
            "for vectorization support")

    def transform(self, sample, corpus=None, tokenizer=None):
        raise NotImplementedError("Override this method" +
            "for vectorization support")


class CountVectorizer(BaseFeatureVectorizer):
    """
        FrequencyCountVectorizers must extend this class
         for vectorization behaviour
    """
    def build_vector(self, corpus):
        raise NotImplementedError("Override this method" +
            "for vectorization support")

    def transform(self, sample, corpus=None, tokenizer=None):
        raise NotImplementedError("Override this method" +
            "for vectorization support")


class BooleanVectorizer(BaseFeatureVectorizer):
    """
        BooleanVectorizers must extend this class for vectorization behaviour
    """
    def build_vector(self, corpus):
        raise NotImplementedError("Override this method" +
            "for vectorization support")

    def transform(self, sample, corpus=None, tokenizer=None):
        raise NotImplementedError("Override this method" +
            "for vectorization support")
