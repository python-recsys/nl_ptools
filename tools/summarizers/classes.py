#-*-coding: utf-8 -*-

from base import BaseSummarizer
import re
import string
from nltk import corpus

stopwords = corpus.stopwords.words('portuguese')


class Summarizer(BaseSummarizer):

    def __init__(self, sentence_tokenizer, paragraph_tokenizer,
                    word_tokenizer, detector):
        self.sentence_tokenizer = sentence_tokenizer
        self.paragraph_tokenizer = paragraph_tokenizer
        self.word_tokenizer = word_tokenizer
        self.detector = detector

    # Return the best sentence in a paragraph
    def get_best_sentence(self, paragraph, sentences_dic):

        # Split the paragraph into sentences
        sentences = self.sentence_tokenizer.tokenize(paragraph)

        # Ignore short paragraphs
        if len(sentences) < 2:
            return ""

        # Get the best sentence according to the sentences dictionary
        best_sentence = ""
        max_value = 0
        for s in sentences:
            strip_s = self.format_sentence(s)
            if strip_s:
                if sentences_dic[strip_s] > max_value:
                    max_value = sentences_dic[strip_s]
                    best_sentence = s

        return best_sentence

    def sentences_intersection(self, sent1, sent2):
        '''
        Caculate the intersection between 2 sentences
        '''
        # split the sentence into words/tokens
        s1 = (map(string.lower, self.word_tokenizer.tokenize(sent1,
                 ascii=True)))
        s2 = (map(string.lower, self.word_tokenizer.tokenize(sent2,
                 ascii=True)))

        s1 = set([word for word in s1 if word not in stopwords])
        s2 = set([word for word in s2 if word not in stopwords])

        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0.0

        # We normalize the result by the average number of words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2.0)

    def get_senteces_ranks(self, query):
        '''
            Convert the content into a dictionary <K, V>
            k = The formatted sentence
            V = The rank of the sentence
        '''
        # Split the content into sentences
        sentences = self.sentence_tokenizer.tokenize(query)

        # Calculate the intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = \
                    self.sentences_intersection(sentences[i], sentences[j])

        # Build the sentences dictionary
        # The score of a sentences is the sum of all its intersection
        sentences_dic = {}
        for i in range(0, n):
            score = 0.0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[self.format_sentence(sentences[i])] = score
        print sentences_dic
        return sentences_dic

    def format_sentence(self, sentence):
        '''
        Format a sentence - remove all non-alphbetic chars from the sentence
        We'll use the formatted sentence as a key in our sentences dictionary
        '''
        sentence = re.sub(r'\W+', '', sentence, re.UNICODE)
        return sentence

    def summarize(self, query):

        #Split the content into paragraphs
        paragraphs = self.paragraph_tokenizer.tokenize(query)

        bag_of_sentences = self.get_senteces_ranks(query)

        print bag_of_sentences

        #Information
        summary = []

        for p in paragraphs:
            sentence = self.get_best_sentence(p, bag_of_sentences).strip()
            if sentence:
                summary.append(sentence)

        return ('\n').join(summary)
