import os

from pyramid.httpexceptions import HTTPNotFound, HTTPNotModified
from kinto.core import Service


here = os.path.abspath(os.path.dirname(__file__))
STATIC_XML_PATH = os.path.join(here, "blocklist.xml")
STATIC_XML_LAST_UPDATE = 1625780281557


PATTERN = (
    "/{prefix}/{api_ver:\\d+}/{application_guid}/{application_ver}/" "{metrics:.*}"
)


blocklist = Service(name="blocklist", path=PATTERN, description="Blocklist data")


@blocklist.get()
def get_blocklist(request):
    prefix = request.matchdict["prefix"]
    if prefix not in request.registry.amo_resources:
        raise HTTPNotFound()

    last_etag = '"{}"'.format(STATIC_XML_LAST_UPDATE)
    request.response.headers["ETag"] = last_etag
    request.response.last_modified = STATIC_XML_LAST_UPDATE / 1000.0

    if_none_match = request.headers.get("If-None-Match")
    if_modified_since = request.headers.get("If-Modified-Since")
    if if_none_match is not None or if_modified_since is not None:
        has_changed = (
            if_none_match != last_etag
            and request.if_modified_since != request.response.last_modified
        )
        if not has_changed:
            response = HTTPNotModified()
            response.headers["ETag"] = last_etag
            response.last_modified = STATIC_XML_LAST_UPDATE / 1000.0
            raise response

    # Serve static XML content.
    with open(STATIC_XML_PATH) as f:
        xml_content = f.read()

    request.response.write(xml_content)
    request.response.content_type = "application/xml;charset=UTF-8"
    return request.response
