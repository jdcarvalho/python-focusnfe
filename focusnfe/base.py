import requests
import json


class FocusNFEException(Exception):
    pass


class FocusNFEBase(object):

    api_key = None
    environment = None

    PRD_URI = 'https://api.focusnfe.com.br/'
    DEV_URI = 'https://homologacao.focusnfe.com.br/v2/nfse'

    ENV_PRODUCTION = 1
    ENV_DEVELOPMENT = 2

    @property
    def base_uri(self):
        if self.environment == FocusNFEBase.ENV_PRODUCTION:
            return FocusNFEBase.PRD_URI
        elif self.environment == FocusNFEBase.ENV_DEVELOPMENT:
            return FocusNFEBase.DEV_URI
        else:
            raise FocusNFEException('Programming Error: Development invalid or not set')

    def __init__(self, api_key, environment):
        self.api_key = api_key
        self.environment = environment

    @staticmethod
    def load_testing_env_variables():
        import os
        from focusnfe.environment import environment
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
        r = response.json()
        if response.status_code in [200, 201]:
            return r
        elif response.status_code == 400:
            raise FocusNFEException('{0} - {1}'.format(r.get('codigo'), r.get('mensagem')))
        elif response.status_code == 403:
            raise FocusNFEException('{0} - {1}'.format(r.get('codigo'), r.get('mensagem')))
        elif response.status_code == 404:
            raise FocusNFEException('{0} - {1}'.format(r.get('codigo'), r.get('mensagem')))
        elif response.status_code == 415:
            raise FocusNFEException('415 - Midia Invalida. JSON Mal formado')
        elif response.status_code == 422:
            raise FocusNFEException('{0} - {1}'.format(r.get('codigo'), r.get('mensagem')))
        elif response.status_code == 429:
            raise FocusNFEException('429 - Excesso de requisicoes atingida. Whoa Cowboy!')
        elif response.status_code == 500:
            raise FocusNFEException('500 - Erro de Servidor')

    def do_get_request(self, url, params):
        pass

    def do_post_request(self, url, params=None):
        params = params if params else {}
        params = {
            'fields': json.dumps(params)
        }
        response = requests.post(url, data=params)
        self.process_errors(response)
        return response

    def do_put_request(self, url, params):
        pass

    def do_delete_request(self, url, params):
        pass
