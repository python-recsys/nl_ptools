#-*-coding: utf-8 -*-
from extractors.base import BaseExtractor
from urllib2 import urlopen
from django.utils import simplejson
from extractors.lib import AlchemyAPI

class DiffbotExtractor(BaseExtractor):

    url = "http://www.diffbot.com/api/article?token=%s&url=%s&format=json"

    def __init__(self, api_key):
        self.api_key = api_key

    def _fetch_url(self, url):
        try:
            result = urlopen(url).read()
        except Exception, e:
            return {'errorCode': 404, 'errors': str(e)}

        return result

    def extract(self, query):
        url = self.url % (self.api_key, query)
        result = self._fetch_url(url)

        json = simplejson.loads(result.decode('utf-8'))

        if 'errorCode' in json:
            dict_result = json
        else:
            text = json['text'] if 'text' in json else ''
            title = json['title'] if 'title' in json else ''
            media = json['media'] if 'media' in json else ''
            resolved_url = json['resolved_url'] if 'resolved_url' in json else ''
            url = json['url'] if 'url' in json else ''

            dict_result = {'text': text, 'title': title, 'media': media,
                'url': url, 'resolved_url': resolved_url}

        return {'response': dict_result}


class AlchemyExtractor(BaseExtractor):

    def __init__(self, api_key):
        self.api_key = api_key
        self.alchemy_api = AlchemyAPI()
        self.alchemy_api.setAPIKey(self.api_key)

    def _fetch_url(self, url):
        try:
            result = self.alchemy_api.URLGetText(url)
        except Exception, e:
            return {'errorCode': 404, 'errors': str(e)}

        return result

    def extract(self, query):
        result = self._fetch_url(query)

        json = simplejson.loads(result.decode('utf-8'))

        if 'errorCode' in json or json['status'] != 'OK':
            dict_result = json
        else:
            text = json['text'] if 'text' in json else ''
            url = json['url'] if 'url' in json else ''
            title = json['title'] if 'title' in json else ''
            media = json['media'] if 'media' in json else ''
            resolved_url = json['resolved_url'] if 'resolved_url' in json else ''

            dict_result = {'text': text, 'title': title, 'media': media,
                'url': url, 'resolved_url': resolved_url}

        return {'response': dict_result}


