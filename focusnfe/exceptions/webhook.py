from focusnfe.core.exception import FocusNFECoreException


class WebHookException(FocusNFECoreException):

    EC_INVALID_CNPJ = 'invalid_cnpj'
    EC_INVALID_EVENT = 'invalid_event'
    EC_INVALID_URL = 'invalid_url'
    EC_INVALID_HOOK = 'invalid_hook'


