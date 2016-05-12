import json
import mock
import os
import xml.etree.ElementTree as ET

from amo2kinto import constants
from kinto_amo.tests.support import AMOTestCase

SERVICE_ENDPOINT = "/blocklist/{api_ver}/{app}/{app_ver}/"

FIXTURES_FILE_NAME = os.path.join(os.path.dirname(__file__), 'fixtures.json')

with open(FIXTURES_FILE_NAME) as fd:
    FIXTURES = json.load(fd)


class AMOTest(AMOTestCase):
    def test_amo_view_returns_xml(self):
        url = SERVICE_ENDPOINT.format(api_ver="3",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="46.0")
        resp = self.app.get(url)
        assert resp.content_type == "application/xml"

    def test_amo_view_only_match_numeric_api_ver(self):
        url = SERVICE_ENDPOINT.format(api_ver="wrong",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="46.0")
        resp = self.app.get(url).maybe_follow(status=404)

        assert resp.content_type == "application/json"

    def test_amo_view_also_match_with_metrics_args(self):
        url = SERVICE_ENDPOINT.format(api_ver="3",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="46.0")
        url += ('PRODUCT/BUILD_ID/BUILD_TARGET/LOCALE/CHANNEL/'
                'OS_VERSION/DISTRIBUTION/DISTRIBUTION_VERSION/'
                'PING_COUNT/TOTAL_PING_COUNT/DAYS_SINCE_LAST_PING/')
        resp = self.app.get(url)

        assert resp.content_type == "application/xml"

    def test_amo_views_passes_api_ver_and_app_args_to_addons_exporter(self):
        with mock.patch('kinto_amo.views.services.write_addons_items') as wai:
            url = SERVICE_ENDPOINT.format(api_ver="3",
                                          app=constants.FIREFOX_APPID,
                                          app_ver="46.0")
            self.app.get(url)
            assert wai.mock_calls[0][2] == {'api_ver': 3,
                                            'app_id': constants.FIREFOX_APPID}

    def test_amo_views_passes_api_and_app_ver_args_to_plugin_exporter(self):
        with mock.patch('kinto_amo.views.services.write_plugin_items') as wpi:
            url = SERVICE_ENDPOINT.format(api_ver="3",
                                          app=constants.FIREFOX_APPID,
                                          app_ver="46.0")
            self.app.get(url)
            assert wpi.mock_calls[0][2] == {'api_ver': 3,
                                            'app_id': constants.FIREFOX_APPID,
                                            'app_ver': "46.0"}

    def test_amo_views_passes_api_and_app_args_to_gfx_exporter(self):
        with mock.patch('kinto_amo.views.services.write_gfx_items') as wgi:
            url = SERVICE_ENDPOINT.format(api_ver="3",
                                          app=constants.FIREFOX_APPID,
                                          app_ver="46.0")
            self.app.get(url)
            assert wgi.mock_calls[0][2] == {'api_ver': 3,
                                            'app_id': constants.FIREFOX_APPID}

    def test_amo_views_passes_api_and_app_args_to_certificates_exporter(self):
        with mock.patch('kinto_amo.views.services.write_cert_items') as wci:
            url = SERVICE_ENDPOINT.format(api_ver="3",
                                          app=constants.FIREFOX_APPID,
                                          app_ver="46.0")
            self.app.get(url)
            assert wci.mock_calls[0][2] == {'api_ver': 3}


class AMOWithFixturesTest(AMOTestCase):
    def setUp(self):
        super(AMOWithFixturesTest, self).setUp()
        self.headers = {
            "Authorization": "Basic YWRtaW46"
        }
        # Create the blocklists bucket
        self.app.put('/buckets/blocklists', headers=self.headers)

        # Create the addons collection
        self.app.put('/buckets/blocklists/collections/addons',
                     headers=self.headers)
        # Create the plugins collection
        self.app.put('/buckets/blocklists/collections/plugins',
                     headers=self.headers)
        # Create the gfx collection
        self.app.put('/buckets/blocklists/collections/gfx',
                     headers=self.headers)
        # Create the certificates collection
        self.app.put('/buckets/blocklists/collections/certificates',
                     headers=self.headers)

        # Create addons records
        url = '/buckets/blocklists/collections/addons/records'
        self.app.post_json(url, {"data": FIXTURES['addons']["enabled"]},
                           headers=self.headers)

        self.app.post_json(url, {"data": FIXTURES['addons']["disabled"]},
                           headers=self.headers)

        # Create plugins records
        url = '/buckets/blocklists/collections/plugins/records'
        self.app.post_json(url, {"data": FIXTURES['plugins']["enabled"]},
                           headers=self.headers)

        self.app.post_json(url, {"data": FIXTURES['plugins']["disabled"]},
                           headers=self.headers)

        # Create gfx records
        url = '/buckets/blocklists/collections/gfx/records'
        self.app.post_json(url, {"data": FIXTURES['gfx']["enabled"]},
                           headers=self.headers)

        self.app.post_json(url, {"data": FIXTURES['gfx']["disabled"]},
                           headers=self.headers)

        # Create certificates records
        url = '/buckets/blocklists/collections/certificates/records'
        resp = self.app.post_json(url, {
            "data": FIXTURES['certificates']["enabled"]
        }, headers=self.headers)

        self.last_modified = resp.json['data']['last_modified']

        self.app.post_json(url, {
            "data": FIXTURES['certificates']["disabled"]
        }, headers=self.headers)

    def test_last_updated_is_taken_from_records(self):
        url = SERVICE_ENDPOINT.format(api_ver="3",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="46.0")
        resp = self.app.get(url)
        xml = ET.fromstring(resp.body)

        blocklist = xml.find('.')
        assert blocklist.get('lastupdate') == str(self.last_modified)

    def test_not_enabled_certificates_are_ignored(self):
        url = SERVICE_ENDPOINT.format(api_ver="3",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="46.0")
        resp = self.app.get(url)
        xml = ET.fromstring(resp.body)
        namespace = '{http://www.mozilla.org/2006/addons-blocklist}'

        certItems = list(xml.findall('./*/{}certItem'.format(namespace)))
        cert_count = len(certItems)
        assert cert_count == 1, 'More than one cert: %s' % certItems

    def test_not_enabled_addons_are_ignored(self):
        url = SERVICE_ENDPOINT.format(api_ver="3",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="46.0")
        resp = self.app.get(url)
        xml = ET.fromstring(resp.body)
        namespace = '{http://www.mozilla.org/2006/addons-blocklist}'

        addons = list(xml.findall('./*/{}emItem'.format(namespace)))
        addons_count = len(addons)
        assert addons_count == 1, 'More than one addon: %s' % addons

    def test_not_enabled_plugins_are_ignored(self):
        url = SERVICE_ENDPOINT.format(api_ver="3",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="46.0")
        resp = self.app.get(url)
        xml = ET.fromstring(resp.body)
        namespace = '{http://www.mozilla.org/2006/addons-blocklist}'

        plugins = list(xml.findall('./*/{}pluginItem'.format(namespace)))
        plugins_count = len(plugins)
        assert plugins_count == 1, 'More than one addon: %s' % plugins

    def test_not_enabled_gfx_are_ignored(self):
        url = SERVICE_ENDPOINT.format(api_ver="3",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="46.0")
        resp = self.app.get(url)
        xml = ET.fromstring(resp.body)
        namespace = '{http://www.mozilla.org/2006/addons-blocklist}'

        gfx = list(xml.findall('./*/{}gfxBlacklistEntry'.format(namespace)))
        gfx_count = len(gfx)
        assert gfx_count == 1, 'More than one addon: %s' % gfx
