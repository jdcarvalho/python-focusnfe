from focusnfe.core import BaseAPIWrapper
from focusnfe.exceptions.nfse import NFSeException


class BaseNFSeWrapper(BaseAPIWrapper):

    PRD_URI = 'https://api.focusnfe.com.br/v2/nfse/{0}'
    DEV_URI = 'https://homologacao.focusnfe.com.br/v2/nfse{0}'

    @property
    def base_uri(self):
        if self.environment == BaseAPIWrapper.ENV_PRODUCTION:
            return BaseNFSeWrapper.PRD_URI
        elif self.environment == BaseAPIWrapper.ENV_DEVELOPMENT:
            return BaseNFSeWrapper.DEV_URI
        else:
            raise NFSeException(
                'Programming Error: Development invalid or not set',
                code=NFSeException.EC_PROGRAMMING,
            )

    def url(self, **kwargs):
        reference = kwargs.pop('reference', '')
        relative = kwargs.pop('relative', '')
        if reference:
            return self.base_uri.format('?ref='+reference)
        elif relative:
            return self.base_uri.format(relative)
        else:
            return self.base_uri.format('')
