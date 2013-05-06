#-*- coding:utf-8 -*-


class BaseSummarizer(object):
    """
        Summarizers must extend this class for summarization behaviour.
    """

    def summarize(self, query):
        raise NotImplementedError("Override this method" +
                "for summarization support")
