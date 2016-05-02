from kinto_amo.tests.support import AMOTestCase


class HelloViewTest(AMOTestCase):

    def test_capability_is_exposed(self):
        resp = self.app.get('/')
        capabilities = resp.json['capabilities']
        self.assertIn('blocklist-xml', capabilities)

        expected = {'url': 'https://github.com/mozilla-services/kinto-amo/',
                    'description': 'An endpoint to generate v2 and v3 XML '
                    'blocklist export.',
                    'resources': {
                        'addons': {'bucket': 'blocklists',
                                   'collection': 'addons'},
                        'plugins': {'bucket': 'blocklists',
                                    'collection': 'plugins'},
                        'gfx': {'bucket': 'blocklists',
                                'collection': 'gfx'},
                        'certificates': {'bucket': 'blocklists',
                                         'collection': 'certificates'}}}
        self.assertEqual(expected, capabilities['blocklist-xml'])
