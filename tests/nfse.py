from unittest import TestCase
import os
from focusnfe.focusnfe import FocusNFE


class NFSeTestCase(TestCase):

    def setUp(self):
        FocusNFE.load_testing_env_variables()
        api_token = os.environ.get('API_TOKEN')
        self.focus = FocusNFE(api_token, FocusNFE.ENV_DEVELOPMENT)

    def test_nfse_creation(self):
        pass
