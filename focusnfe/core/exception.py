
class FocusNFECoreException(Exception):

    EC_PROGRAMMING = 'programming_error'
    EC_BAD_REQUEST = 'bad_request'
    EC_FORBIDDEN = 'forbidden'
    EC_NOT_FOUND = 'not_found'
    EC_SERVER_ERROR = 'server_error'

    code = None

    def __init__(self, *args, **kwargs):
        self.code = kwargs.pop('code')
        super(FocusNFECoreException, self).__init__(*args, **kwargs)
