import mock
import xml.etree.ElementTree as ET

from kinto2xml import constants
from kinto_amo.tests.support import AMOTestCase

SERVICE_ENDPOINT = "/blocklist/{api_ver}/{app}/{app_ver}/"


class AMOTest(AMOTestCase):
    def test_amo_view_returns_xml(self):
        url = SERVICE_ENDPOINT.format(api_ver="3",
                                      app=constants.FIREFOX_APPID,
                                      app_ver="46.0")
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
        self.app.post_json(url, {"data": {
            "guid": "{0153E448-190B-4987-BDE1-F256CADA672F}",
            "blockID": "i914",
            "enabled": True,
            "details": {
                "who": "All Firefox users who have this add-on installed.",
                "created": "2015-06-02T09:56:58Z",
                "bug": "https://bugzilla.mozilla.org/show_bug.cgi?id=1170633",
                "name": "RealPlayer Browser Record Plugin",
                "why": "Some versions of this extension are causing crashes."},
            "versionRange": [{
                "targetApplication": [{
                    "minVersion": "39.0a1",
                    "guid": "{ec8030f7-c20a-464f-9b0e-13a3a9e97384}",
                    "maxVersion": "*"}],
                "minVersion": "0",
                "maxVersion": "*",
                "severity": 3}],
            "prefs": []
        }}, headers=self.headers)

        self.app.post_json(url, {"data": {
            "guid": "{cc8f597b-0765-404e-a575-82aefbd81daf}",
            "blockID": "i380",
            "enabled": False,
            "details": {
                "who": "All Firefox users who have this add-on installed.",
                "created": "2013-06-19T13:03:00Z",
                "bug": "https://bugzilla.mozilla.org/show_bug.cgi?id=866332",
                "name": "Update My Browser (malware)",
                "why": "This is a malicious add-on."},
            "versionRange": [{
                "targetApplication": [],
                "minVersion": "0",
                "maxVersion": "*",
                "severity": 3}],
            "prefs": []
        }}, headers=self.headers)

        # Create plugins records
        url = '/buckets/blocklists/collections/plugins/records'
        self.app.post_json(url, {"data": {
            "infoURL": "https://get.adobe.com/flashplayer/",
            "blockID": "p160",
            "enabled": True,
            "matchFilename": "NPSWF32\\.dll",
            "details": {
                "who": "All Firefox users who have this plugin installed.",
                "created": "2012-10-05T12:34:22Z",
                "bug": "https://bugzilla.mozilla.org/show_bug.cgi?id=797378",
                "name": "Adobe Flash 10.2.* and lower",
                "why": "This plugin is outdated and is potentially insecure."},
            "versionRange": [{
                "targetApplication": [{
                    "minVersion": "4.0",
                    "guid": "{ec8030f7-c20a-464f-9b0e-13a3a9e97384}",
                    "maxVersion": "16.*"}],
                "minVersion": "0",
                "maxVersion": "10.2.9999",
                "severity": 0,
                "vulnerabilityStatus": 1}]
        }}, headers=self.headers)

        self.app.post_json(url, {"data": {
            "blockID": "p152",
            "enabled": False,
            "matchFilename": "npctrl\\.dll",
            "details": {
                "who": "All Firefox users who have this plugin installed.",
                "created": "2012-10-05T10:34:12Z",
                "bug": "https://bugzilla.mozilla.org/show_bug.cgi?id=797378",
                "name": "Silverlight 4.1.10328.0 and lower",
                "why": "This plugin is outdated and is potentially insecure."},
            "versionRange": [{
                "targetApplication": [],
                "minVersion": "0",
                "maxVersion": "4.1.10328.0",
                "severity": 0,
                "vulnerabilityStatus": 1}]
        }}, headers=self.headers)

        # Create gfx records
        url = '/buckets/blocklists/collections/gfx/records'
        self.app.post_json(url, {"data": {
            "vendor": "0x10de",
            "blockID": "g200",
            "enabled": True,
            "feature": "WEBGL_MSAA",
            "devices": [],
            "featureStatus": "BLOCKED_DEVICE",
            "details": {
                "who": "All Firefox users.",
                "created": "2012-11-12T10:35:32Z",
                "bug": "https://bugzilla.mozilla.org/show_bug.cgi?id=809550",
                "name": "Mac OS X WebGL anti-aliasing",
                "why": "Security problems."},
            "os": "Darwin 11"
        }}, headers=self.headers)

        self.app.post_json(url, {"data": {
            "driverVersionComparator": "EQUAL",
            "driverVersion": "8.15.10.2086",
            "vendor": "0x8086",
            "blockID": "g1124",
            "enabled": False,
            "devices": ["0x2a42", "0x2e22", "0x2e12", "0x2e32", "0x0046"],
            "featureStatus": "BLOCKED_DRIVER_VERSION",
            "details": {
                "who": ".",
                "created": "2016-02-22T23:40:14Z",
                "bug": "https://bugzilla.mozilla.org/show_bug.cgi?id=1170143",
                "name": "Intel Driver 8.15.10.2086",
                "why": "."},
            "os": "All"
        }}, headers=self.headers)

        # Create certificates records
        url = '/buckets/blocklists/collections/certificates/records'
        resp = self.app.post_json(url, {"data": {
            "serialNumber": "UoRGnb96CUDTxIqVry6LBg==",
            "enabled": True,
            "details": {
                "who": ".",
                "created": "2015-04-07T11:04:11Z",
                "bug": "https://bugzilla.mozilla.org/show_bug.cgi?id=1150585",
                "name": "XS4ALL certificate",
                "why": "."},
            "issuerName": "MIGQMQswCQYDVQQGEwJHQjEbMBkGA1U...NB"
        }}, headers=self.headers)

        self.last_modified = resp.json['data']['last_modified']

        self.app.post_json(url, {"data": {
            "serialNumber": "NMpMcEnex3eXx4ohk9glcQ==",
            "enabled": False,
            "details": {
                "who": ".",
                "created": "2016-03-01T21:22:27Z",
                "bug": "https://bugzilla.mozilla.org/show_bug.cgi?id=1252142",
                "name": "exceptional SHA-1 Certificates",
                "why": "."},
            "issuerName": "MI...yIENBIC0gRzM="
        }}, headers=self.headers)

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
