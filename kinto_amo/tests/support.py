import os
import webtest

from kinto.tests.core import support as kinto_support
from kinto.tests.core.support import unittest


class AMOTestCase(unittest.TestCase):
    def setUp(self):
        super(AMOTestCase, self).setUp()
        self.config = 'config.ini'
        curdir = os.path.dirname(os.path.realpath(__file__))
        app = webtest.TestApp("config:%s" % self.config, relative_to=curdir)
        app.RequestClass = kinto_support.get_request_class(prefix="v1")
        self.app = app
