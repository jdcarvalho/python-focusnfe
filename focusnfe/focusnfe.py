from focusnfe.base import BaseFocusNFEBase
from focusnfe.api.nfse import Nfse


class FocusNFE(BaseFocusNFEBase):

    _nfse = None

    @property
    def nfse(self):
        if not self._nfse:
            self._nfse = Nfse(self.api_key, self.environment)
        return self._nfse
