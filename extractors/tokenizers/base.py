import re
from extractors.utils import asciize


class TokenizerException(Exception):
    pass


class BaseTokenizer(object):

    '''
    Tokenizer for News/Blog headlines that
    ignores most punctuation and simply
    returns the words.
    The tokens can then be further processed with
    the Keyword Tagger for example.
    '''

    # Scanner callbacks...
    def word_(scanner, token):
        return "WORD", token

    scanner = re.Scanner([
        (r"\W+", None),
        (r"\b\w+\b", word_),
        ], re.UNICODE)

    @classmethod
    def tokenize(cls, text, ascii=False):
        tokens, remainder = cls.scanner.scan(text)
        if remainder:
            print "****input failed syntax*****"
            print "tokens:%s" % str(tokens)
            print "remainder:%s" % remainder
            raise TokenizerException
        include = ("WORD",)
        tokens = [t[1] if not ascii else asciize(t[1])
                    for t in tokens if t[0] in include]
        return tokens
