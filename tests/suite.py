from unittest import TestSuite
from tests import NFSeTestCase


class FocusNFSeTests(TestSuite):

    def __init__(self, *args, **kwargs):
        super(FocusNFSeTests, self).__init__(*args, **kwargs)
        self.addTest(NFSeTestCase)
