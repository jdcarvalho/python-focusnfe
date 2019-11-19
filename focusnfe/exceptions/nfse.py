from focusnfe.core.exception import FocusNFECoreException


class NFSeException(FocusNFECoreException):

    EC_ALREADY_AUTHORIZED = 'already_authorized'
    EC_WHOA_COWBOY = 'whoa_cowboy'

    EC_INVALID_NATURE = 'no_nature'
    EC_INVALID_RAZAO = 'invalid_razao'
    EC_INVALID_CNPJ = 'invalid_cnpj'
    EC_INVALID_REGIME = 'invalid_regime'
    EC_INVALID_PRESTADOR = 'invalid_prestador'
    EC_INVALID_TOMADOR = 'invalid_tomador'
    EC_INVALID_SERVICE = 'invalid_service'


