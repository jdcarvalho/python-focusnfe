import json

from focusnfe.core import BaseAPIWrapper
from focusnfe.exceptions.webhook import WebHookException


class WebHook(BaseAPIWrapper):
    PRD_URI = 'https://api.focusnfe.com.br/v2/hooks'
    DEV_URI = 'https://homologacao.focusnfe.com.br/v2/hooks'

    EVENT_NFE = 'nfe'
    EVENT_NFSE = 'nfse'

    ALL_EVENTS = [
        EVENT_NFE,
        EVENT_NFSE
    ]

    @property
    def base_uri(self):
        try:
            if int(self.environment) == BaseAPIWrapper.ENV_PRODUCTION:
                return WebHook.PRD_URI
            elif int(self.environment) == BaseAPIWrapper.ENV_DEVELOPMENT:
                return WebHook.DEV_URI
            else:
                raise WebHookException(
                    'Programming Error: Development invalid or not set',
                    code=WebHookException.EC_PROGRAMMING,
                )
        except:
            raise WebHookException(
                'Programming Error: Development invalid or not set',
                code=WebHookException.EC_PROGRAMMING,
            )

    def url(self, **kwargs):
        reference = kwargs.pop('reference', '')
        relative = kwargs.pop('relative', '')
        if reference:
            return self.base_uri.format('?ref=' + reference)
        elif relative:
            return self.base_uri.format(relative)
        else:
            return self.base_uri.format('')

    def __prepare_webhook(self, **kwargs):
        mandatory = [
            'cnpj',
            'event',
            'url',
        ]
        for arg in mandatory:
            if arg not in kwargs:
                raise WebHookException(
                    'Argumento {0} não enviado no serviço'.format(arg),
                    code=WebHookException.EC_INVALID_HOOK,
                )

        cnpj = kwargs.pop('cnpj', '')
        cnpj = self.digits_only(cnpj)
        if cnpj and len(cnpj) != 14:
            raise WebHookException(
                '[{0}]: CNPJ informado inválido'.format(cnpj),
                code=WebHookException.EC_INVALID_CNPJ
            )

        event = kwargs.pop('event', '')
        if event not in WebHook.ALL_EVENTS:
            raise WebHookException(
                'Event inválido. Valores aceitáveis são [{1}]'.format(
                    event, ','.join(WebHook.ALL_EVENTS)
                ),
                code=WebHookException.EC_INVALID_EVENT)

        url = kwargs.pop('url', '')
        if not url:
            raise WebHookException(
                '[{0}]: URL para gatilho não informada'.format('url'),
                code=WebHookException.EC_INVALID_URL
            )

        payload = {
            'cnpj': cnpj,
            'event': event,
            'url': url,
        }

        return payload

    def create_webhook(self, **kwargs):
        payload_dict = self.__prepare_webhook(**kwargs)
        payload = json.dumps(payload_dict)
        response = self.do_post_request(self.url(), data=payload)
        return response
