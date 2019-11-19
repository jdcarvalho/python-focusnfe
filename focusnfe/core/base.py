import requests

from focusnfe.exceptions.nfse import NFSeException


class BaseAPIWrapper(object):

    api_key = None
    environment = None

    ENV_PRODUCTION = 1
    ENV_DEVELOPMENT = 2

    def digits_only(self, value):
        if isinstance(value, str):
            aux = [str(s) for s in value if s.isdigit()]
            return ''.join(aux)
        else:
            return ''

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
            raise NFSeException(
                '{0} - {1}'.format(r.get('codigo'), r.get('mensagem')),
                code=NFSeException.EC_BAD_REQUEST
            )
        elif response.status_code == 403:
            raise NFSeException(
                '{0} - {1}'.format(r.get('codigo'), r.get('mensagem')),
                code=NFSeException.EC_FORBIDDEN
            )
        elif response.status_code == 404:
            raise NFSeException(
                '{0} - {1}'.format(r.get('codigo'), r.get('mensagem')),
                code=NFSeException.EC_NOT_FOUND
            )
        elif response.status_code == 415:
            raise NFSeException(
                '415 - Midia Invalida. JSON Mal formado',
                code=NFSeException.EC_BAD_REQUEST,
            )
        elif response.status_code == 422:
            raise NFSeException(
                '{0} - {1}'.format(r.get('codigo'), r.get('mensagem')),
                code=NFSeException.EC_ALREADY_AUTHORIZED,
            )
        elif response.status_code == 429:
            raise NFSeException(
                '429 - Excesso de requisicoes atingida. Whoa Cowboy!',
                code=NFSeException.EC_WHOA_COWBOY,
            )
        elif response.status_code == 500:
            raise NFSeException(
                '500 - Erro de Servidor',
                code=NFSeException.EC_SERVER_ERROR,
            )

    def do_get_request(self, url, params=None, data=None):
        r = requests.get(url, params=params, auth=(self.api_key, ""))
        return self.process_errors(response=r)

    def do_post_request(self, url, params=None, data=None):
        r = requests.post(url, params=params, data=data, auth=(self.api_key, ""))
        return self.process_errors(response=r)

    def do_delete_request(self, url, data=None):
        r = requests.delete(url, data=data, auth=(self.api_key, ""))
        return self.process_errors(response=r)
