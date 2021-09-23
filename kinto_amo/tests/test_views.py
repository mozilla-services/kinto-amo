from kinto_amo.tests.support import AMOTestCase


SERVICE_ENDPOINT = "/blocklist/{api_ver}/{app}/{app_ver}/"

FIREFOX_APPID = "{3550f703-e582-4d05-9a08-453d09bdfdc6}"


class AMOTest(AMOTestCase):
    url = SERVICE_ENDPOINT.format(api_ver="3", app=FIREFOX_APPID, app_ver="46.0")

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

    def test_amo_view_only_match_blocklist_or_preview(self):
        resp = self.app.get(self.url.replace("blocklist", "unknown")).maybe_follow(
            status=404
        )

        assert resp.content_type == "application/json"

    def test_amo_view_only_match_numeric_api_ver(self):
        url = SERVICE_ENDPOINT.format(
            api_ver="wrong", app=FIREFOX_APPID, app_ver="46.0"
        )
        resp = self.app.get(url).maybe_follow(status=404)

        assert resp.content_type == "application/json"

    def test_amo_view_also_match_with_metrics_args(self):
        url = self.url + (
            "PRODUCT/BUILD_ID/BUILD_TARGET/LOCALE/CHANNEL/"
            "OS_VERSION/DISTRIBUTION/DISTRIBUTION_VERSION/"
            "PING_COUNT/TOTAL_PING_COUNT/DAYS_SINCE_LAST_PING/"
        )
        resp = self.app.get(url)

        assert resp.content_type == "application/xml"
