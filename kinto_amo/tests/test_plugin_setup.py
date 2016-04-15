from kinto_amo.tests.support import AMOTestCase


class HelloViewTest(AMOTestCase):

    def test_capability_is_exposed(self):
        resp = self.app.get('/')
        capabilities = resp.json['capabilities']
        self.assertIn('amo', capabilities)

        expected = {u'url': u'https://github.com/mozilla-services/kinto-amo/',
                    u'description': u'AMO-style API for Kinto'}
        self.assertEqual(expected, capabilities['amo'])
