import json
import mock
import os
import pytest
import xml.etree.ElementTree as ET

from amo2kinto import constants
from kinto_amo.tests.support import AMOTestCase
from pyramid.exceptions import ConfigurationError


SERVICE_ENDPOINT = "/blocklist/{api_ver}/{app}/{app_ver}/"

FIXTURES_FILE_NAME = os.path.join(os.path.dirname(__file__), 'fixtures.json')

with open(FIXTURES_FILE_NAME) as fd:
    FIXTURES = json.load(fd)


class AMOTest(AMOTestCase):
    url = SERVICE_ENDPOINT.format(api_ver="3",
                                  app=constants.FIREFOX_APPID,
                                  app_ver="46.0")

    def test_amo_view_returns_xml(self):
        resp = self.app.get(self.url)
        assert resp.content_type == "application/xml"

    def test_has_etag_response_header(self):
        resp = self.app.get(self.url)
        assert "ETag" in resp.headers

    def test_has_last_modified_response_header(self):
        resp = self.app.get(self.url)
        assert "Last-Modified" in resp.headers

    def test_returns_304_if_not_modified_since(self):
        resp = self.app.get(self.url)
        last_etag = resp.headers["ETag"]
        last_modified = resp.headers["Last-Modified"]

        resp = self.app.get(self.url, headers={"If-None-Match": last_etag})
        assert resp.status_code == 304

        resp = self.app.get(self.url, headers={"If-Modified-Since": last_modified})
        assert resp.status_code == 304

    def test_returns_200_if_not_modified_since_is_malformed(self):
        # We don't want to break clients.
        resp = self.app.get(self.url, headers={"If-Modified-Since": "semaine derniere"})
        assert resp.status_code == 200

    def test_returns_200_if_none_match_is_malformed(self):
        # We don't want to break clients.
        resp = self.app.get(self.url, headers={"If-None-Match": "42a"})
        assert resp.status_code == 200

    def test_amo_view_only_match_numeric_api_ver(self):
        url = SERVICE_ENDPOINT.format(api_ver="wrong",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="46.0")
        resp = self.app.get(url).maybe_follow(status=404)

        assert resp.content_type == "application/json"

    def test_amo_view_also_match_with_metrics_args(self):
        url = self.url + ('PRODUCT/BUILD_ID/BUILD_TARGET/LOCALE/CHANNEL/'
                          'OS_VERSION/DISTRIBUTION/DISTRIBUTION_VERSION/'
                          'PING_COUNT/TOTAL_PING_COUNT/DAYS_SINCE_LAST_PING/')
        resp = self.app.get(url)

        assert resp.content_type == "application/xml"

    def test_amo_views_passes_api_ver_and_app_args_to_addons_exporter(self):
        with mock.patch('kinto_amo.views.services.write_addons_items') as wai:
            self.app.get(self.url)
            assert wai.mock_calls[0][2] == {'api_ver': 3,
                                            'app_id': constants.FIREFOX_APPID,
                                            'app_ver': "46.0"}

    def test_amo_views_passes_api_and_app_ver_args_to_plugin_exporter(self):
        with mock.patch('kinto_amo.views.services.write_plugin_items') as wpi:
            self.app.get(self.url)
            assert wpi.mock_calls[0][2] == {'api_ver': 3,
                                            'app_id': constants.FIREFOX_APPID,
                                            'app_ver': "46.0"}

    def test_amo_views_passes_api_and_app_args_to_gfx_exporter(self):
        with mock.patch('kinto_amo.views.services.write_gfx_items') as wgi:
            self.app.get(self.url)
            assert wgi.mock_calls[0][2] == {'api_ver': 3,
                                            'app_id': constants.FIREFOX_APPID}

    def test_amo_views_passes_api_and_app_args_to_certificates_exporter(self):
        with mock.patch('kinto_amo.views.services.write_cert_items') as wci:
            self.app.get(self.url)
            assert wci.mock_calls[0][2] == {'api_ver': 3,
                                            'app_id': constants.FIREFOX_APPID,
                                            'app_ver': "46.0"}


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

        # Create many certificates records
        url = '/buckets/blocklists/collections/certificates/records'
        for i in range(100):
            resp = self.app.post_json(url, {
                "data": FIXTURES['certificates']["enabled"]
            }, headers=self.headers)
            self.last_modified = resp.json['data']['last_modified']

        # And one last disable one.
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
        assert cert_count == 100, 'More than 100 certs: %s' % certItems

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

    def test_outdated_addons_are_ignored(self):
        url = SERVICE_ENDPOINT.format(api_ver="3",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="58.0")
        resp = self.app.get(url)
        xml = ET.fromstring(resp.body)
        namespace = '{http://www.mozilla.org/2006/addons-blocklist}'

        addons = list(xml.findall('./*/{}emItem'.format(namespace)))
        addons_count = len(addons)
        assert addons_count == 0, 'Unexpected add-ons found: %s' % addons

    def test_outdated_plugins_are_ignored(self):
        url = SERVICE_ENDPOINT.format(api_ver="3",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="58.0")
        resp = self.app.get(url)
        xml = ET.fromstring(resp.body)
        namespace = '{http://www.mozilla.org/2006/addons-blocklist}'

        plugins = list(xml.findall('./*/{}pluginItem'.format(namespace)))
        plugins_count = len(plugins)
        assert plugins_count == 0, 'Unexpected plugins found: %s' % plugins

    def test_no_certs_after_firefox_58(self):
        url = SERVICE_ENDPOINT.format(api_ver="3",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="58.0")
        resp = self.app.get(url)
        xml = ET.fromstring(resp.body)
        namespace = '{http://www.mozilla.org/2006/addons-blocklist}'

        certs = list(xml.findall('./*/{}certitem'.format(namespace)))
        cert_count = len(certs)
        assert cert_count == 0, 'Unexpected certs found: %s' % certs


class AMOCustomTest(AMOTestCase):

    @classmethod
    def get_app_settings(cls, extras=None):
        settings = super().get_app_settings(extras)
        settings['amo.preview.addons'] = '/buckets/blocklists/collections/addons'
        settings['amo.preview.plugins'] = '/buckets/blocklists/collections/plugins'
        settings['amo.preview.gfx'] = '/buckets/blocklists/collections/gfx'
        settings['amo.preview.certificates'] = '/buckets/blocklists/collections/certificates'
        return settings

    def test_returns_a_404_when_the_resource_is_not_defined(self):
        url = SERVICE_ENDPOINT.replace('blocklist', 'unknown') \
                              .format(api_ver="3",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="46.0")
        self.app.get(url).follow(status=404)

    def test_get_the_preview_resource_is_defined(self):
        url = SERVICE_ENDPOINT.replace('blocklist', 'preview') \
                              .format(api_ver="3",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="46.0")
        self.app.get(url, status=200)


class AMOSetupFailureTest(AMOTestCase):

    def test_configuration_error_when_blocklist_resource_missing(self):
        settings = {
            'amo.preview.addons': '/buckets/blocklists/collections/addons',
            'amo.preview.plugins': '/buckets/blocklists/collections/plugins'
        }

        with pytest.raises(ConfigurationError):
            self.make_app(settings)

    def test_configuration_error_when_unknown_blocklist_resource_present(self):
        settings = {
            'amo.preview.addons': '/buckets/blocklists/collections/addons',
            'amo.preview.plugins': '/buckets/blocklists/collections/plugins',
            'amo.preview.gfx': '/buckets/blocklists/collections/gfx',
            'amo.preview.certificates': '/buckets/blocklists/collections/certificates',
            'amo.preview.unknown': 'should fail',
        }

        with pytest.raises(ConfigurationError):
            self.make_app(settings)
