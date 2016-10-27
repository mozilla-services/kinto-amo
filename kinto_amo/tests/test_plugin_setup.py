from kinto_amo import __version__ as amo_version
from kinto_amo.tests.support import AMOTestCase


class HelloViewTest(AMOTestCase):

    def test_capability_is_exposed(self):
        self.maxDiff = None
        resp = self.app.get('/')
        capabilities = resp.json['capabilities']
        self.assertIn('blocklist-xml', capabilities)

        expected = {'url': 'https://github.com/mozilla-services/kinto-amo/',
                    'description': 'An endpoint to generate v2 and v3 XML '
                    'blocklist export.',
                    'version': amo_version,
                    'resources': {
                        'blocklist': {
                            'addons': {'bucket': 'blocklists',
                                       'collection': 'addons'},
                            'plugins': {'bucket': 'blocklists',
                                        'collection': 'plugins'},
                            'gfx': {'bucket': 'blocklists',
                                    'collection': 'gfx'},
                            'certificates': {'bucket': 'blocklists',
                                             'collection': 'certificates'}}}}
        self.assertEqual(expected, capabilities['blocklist-xml'])
