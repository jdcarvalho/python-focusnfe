from focusnfe.api.webhook import WebHook
from focusnfe.core.base import BaseAPIWrapper
from focusnfe.api.cte import CTe
from focusnfe.api.mdfe import MDFe
from focusnfe.api.nfce import NFCe
from focusnfe.api.nfe import NFe
from focusnfe.api.nfse import Nfse


class FocusNFE(BaseAPIWrapper):

    _nfse = None
    _nfe = None
    _cte = None
    _mdfe = None
    _nfce = None
    _webhook = None

    @property
    def nfse(self):
        if not self._nfse:
            self._nfse = Nfse(self.api_key, self.environment)
        return self._nfse

    @property
    def nfe(self):
        if not self._nfe:
            self._nfe = NFe(self.api_key, self.environment)
        return self._nfe

    @property
    def cte(self):
        if not self._cte:
            self._cte = CTe(self.api_key, self.environment)
        return self._cte

    @property
    def mdfe(self):
        if not self._mdfe:
            self._mdfe = MDFe(self.api_key, self.environment)
        return self._mdfe

    @property
    def nfce(self):
        if not self._nfce:
            self._nfce = NFCe(self.api_key, self.environment)
        return self._nfce

    @property
    def webhook(self):
        if not self._webhook:
            self._webhook = WebHook(self.api_key, self.environment)
        return self._webhook

