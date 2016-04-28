import mock

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
