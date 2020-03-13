import os
from unittest import TestCase

from focusnfe.api.webhook import WebHook
from focusnfe.focusnfe import FocusNFE


class WebHookTestCase(TestCase):

    def setUp(self):
        api_token = os.environ.get('API_TOKEN')
        self.focus = FocusNFE(api_token, os.environ.get('ENVIRONMENT'))

    def test_create_hook_invalid_cnpj(self):
        from focusnfe.exceptions.webhook import WebHookException
        try:
            self.focus.webhook.create_webhook(
                cnpj='213.213',
            )
        except WebHookException as e:
            self.assertTrue(e.code == WebHookException.EC_INVALID_CNPJ)

    def test_create_hook_invalid_event(self):
        from focusnfe.exceptions.webhook import WebHookException
        try:
            self.focus.webhook.create_webhook(
                cnpj='13.861.761/0001-80',
                event='',
            )
        except WebHookException as e:
            self.assertTrue(e.code == WebHookException.EC_INVALID_EVENT)

    def test_create_hook_invalid_url(self):
        from focusnfe.exceptions.webhook import WebHookException
        try:
            self.focus.webhook.create_webhook(
                cnpj='13.861.761/0001-80',
                event=WebHook.EVENT_NFSE,
                url='',
            )
        except WebHookException as e:
            self.assertTrue(e.code == WebHookException.EC_INVALID_URL)

    def test_create_hook(self):
        r = self.focus.webhook.create_webhook(
            self.focus.webhook.create_webhook(
                cnpj='13.861.761/0001-80',
                event=WebHook.EVENT_NFSE,
                url='http://minhaurl.com/nfse',
            )
        )
        self.assertTrue(r.status_code in [200, 201])
