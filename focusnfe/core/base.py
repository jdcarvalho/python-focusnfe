import requests

from focusnfe.core.exception import FocusNFECoreException
from focusnfe.exceptions.nfse import NFSeException


class BaseAPIWrapper(object):
    api_key = None
    environment = None

    ENV_PRODUCTION = 1
    ENV_DEVELOPMENT = 2

    URI_PRODUCTION = 'https://api.focusnfe.com.br/'
    URI_DEVELOPMENT = 'https://homologacao.focusnfe.com.br/'

    def __init__(self, api_key, environment):
        self.api_key = api_key
        self.environment = environment

    @property
    def base_uri(self):
        try:
            if int(self.environment) == BaseAPIWrapper.ENV_PRODUCTION:
                return self.URI_PRODUCTION
            elif int(self.environment) == BaseAPIWrapper.ENV_DEVELOPMENT:
                return self.URI_DEVELOPMENT
            else:
                raise FocusNFECoreException(
                    'Programming Error: Development invalid or not set',
                    code=FocusNFECoreException.EC_PROGRAMMING,
                )
        except:
            raise FocusNFECoreException(
                'Programming Error: Development invalid or not set',
                code=FocusNFECoreException.EC_PROGRAMMING,
            )

    def url(self, **kwargs):
        raise FocusNFECoreException(
            'Programming Error: Url not implemented',
            code=FocusNFECoreException.EC_PROGRAMMING
        )

    def digits_only(self, value):
        if isinstance(value, str):
            aux = [str(s) for s in value if s.isdigit()]
            return ''.join(aux)
        else:
            return ''

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
        if response.status_code in [200, 201, 202]:
            r = response.json()
            r.update({'status_code': response.status_code})
            return r
        elif response.status_code == 400:
            raise FocusNFECoreException(
                '{0} - {1}'.format(response.status_code, response.text),
                code=FocusNFECoreException.EC_BAD_REQUEST
            )
        elif response.status_code == 401:
            raise FocusNFECoreException(
                'Requisição não autorizada {0} - {1}'.format(response.status_code, response.text),
                code=NFSeException.EC_FORBIDDEN
            )
        elif response.status_code == 403:
            raise FocusNFECoreException(
                '{0} - {1}'.format(response.status_code, response.text),
                code=FocusNFECoreException.EC_FORBIDDEN
            )
        elif response.status_code == 404:
            raise FocusNFECoreException(
                '{0} - {1}'.format(response.status_code, response.text),
                code=FocusNFECoreException.EC_NOT_FOUND
            )
        elif response.status_code == 415:
            raise FocusNFECoreException(
                '{0} - Midia Invalida. JSON Mal formado'.format(response.status_code),
                code=FocusNFECoreException.EC_BAD_REQUEST,
            )
        elif response.status_code == 422:
            raise NFSeException(
                '{0} - {1}'.format(response.status_code, response.text),
                code=NFSeException.EC_ALREADY_AUTHORIZED,
            )
        elif response.status_code == 429:
            raise NFSeException(
                '{0} - Excesso de requisicoes atingida. Whoa Cowboy!'.format(response.status_code),
                code=NFSeException.EC_WHOA_COWBOY,
            )
        elif response.status_code == 500:
            raise FocusNFECoreException(
                '{0} - Erro de Servidor'.format(response.status_code),
                code=FocusNFECoreException.EC_SERVER_ERROR,
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
