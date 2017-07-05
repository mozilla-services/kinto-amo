import os
import unittest

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from kinto import main as kinto_main
from kinto.core.testing import BaseWebTest

HERE = os.path.dirname(os.path.abspath(__file__))


class AMOTestCase(BaseWebTest, unittest.TestCase):
    api_prefix = "v1"
    entry_point = kinto_main
    config = 'config.ini'

    @classmethod
    def get_app_settings(cls, extras=None):
        ini_path = os.path.join(HERE, cls.config)
        config = configparser.ConfigParser()
        config.read(ini_path)
        settings = dict(config.items('app:main'))
        if extras:
            settings.update(extras)
        return settings
