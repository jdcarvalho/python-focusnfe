from focusnfe.core.exception import FocusNFECoreException


class NFSeException(FocusNFECoreException):

    EC_ALREADY_AUTHORIZED = 'already_authorized'
    EC_WHOA_COWBOY = 'whoa_cowboy'

