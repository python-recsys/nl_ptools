from extractors.base import BaseDetector
from extractors.lib import AlchemyAPI
from django.utils import simplejson
from lib import Lid


class AlchemyLangDetector(BaseDetector):

    def __init__(self, api_key):
        self.api_key = api_key
        self.alchemy_api = AlchemyAPI()
        self.alchemy_api.setAPIKey(self.api_key)

    def _fetch_url(self, url):
        try:
            result = self.alchemy_api.URLGetLanguage(url)
        except Exception, e:
            return {'errorCode': 404, 'errors': str(e)}
        return result

    def _fetch_text(self, url):
        try:
            result = self.alchemy_api.TextGetLanguage(url)
        except Exception, e:
            return {'errorCode': 404, 'errors': str(e)}
        return result

    def language(self, query):
        if query.startswith('www') or query.startswith('http'):
            result = self._fetch_url(query)

            json = simplejson.loads(result.decode('utf-8'))

            if 'errorCode' in json or json['status'] != 'OK':
                dict_result = json
            else:
                lang = json['language'] if 'language' in json else ''
                alpha1 = json['iso-639-1'] if 'iso-639-1' in json else ''
                url = json['url'] if 'url' in json else ''

                dict_result = {'language': lang, 'alpha1': alpha1}

            return {'response': {'languages': [dict_result], 'url': url}}

        else:
            result = self._fetch_text(query)

            json = simplejson.loads(result.decode('utf-8'))

            if 'errorCode' in json or json['status'] != 'OK':
                dict_result = json
            else:
                lang = json['language'] if 'language' in json else ''
                alpha1 = json['iso-639-1'] if 'iso-639-1' in json else ''

                dict_result = {'language': lang, 'alpha1': alpha1}

            return {'response': {'languages': [dict_result], 'text': query}}


class NaiveLangDetector(BaseDetector):

    def __init__(self):
        self.lid = Lid()

    def language(self, query):
        if query.startswith('www') or query.startswith('http'):
            raise NotImplementedError('For URL It does not work yet.')
        else:
            result = self.lid.checkText(query)

            dict_result = {'language': result['language']}

            return {'response': {'languages': [dict_result], 'text': query}}
