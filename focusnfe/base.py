import requests
import json


class NotazzException(Exception):
    pass


class NotazzBase(object):

    api_key = None

    PRD_URI = 'https://app.notazz.com/api/'

    @property
    def base_uri(self):
        return NotazzBase.PRD_URI

    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def load_testing_env_variables():
        import os
        from notazz.environment import environment
        for key, value in environment:
            try:
                os.environ.setdefault(key, value)
            except:
                print('Error on key', key)

    def process_errors(self, response):
        """
        :param response:
        :return:
        """
        if response.status_code:
            r = response.json()
            if 'codigoProcessamento' in r:
                code = r.get('codigoProcessamento')
                if str(code) != '000':
                    desc = r.get('motivo')
                    raise NotazzException('{code} - {desc}'.format(
                        code=code,
                        desc=desc,
                    ))
        elif response.status_code == 401:
            raise NotazzException('Auth Error: 401 - API key missing')
        elif response.status_code == 403:
            raise NotazzException('Teje Preso!')
        elif response.status_code == 404:
            raise NotazzException('Programming error: 404 - URI not found')
        elif response.status_code == 500:
            raise NotazzException('500 -Something wrong with Notazz Server')

    def do_post_request(self, url, params=None):
        params = params if params else {}
        params = {
            'fields': json.dumps(params)
        }
        response = requests.post(url, data=params)
        self.process_errors(response)
        return response

