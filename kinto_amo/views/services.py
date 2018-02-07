from pyramid.httpexceptions import HTTPNotFound, HTTPNotModified
from kinto.core import Service, utils
from kinto.core.storage import Filter

from amo2kinto.exporter import (
    write_addons_items, write_plugin_items, write_gfx_items, write_cert_items
)
from lxml import etree

path = ('/{prefix}/{api_ver:\d+}/{application_guid}/{application_ver}/'
        '{metrics:.*}')

PARENT_PATTERN = "/buckets/{bucket}/collections/{collection}"

blocklist = Service(name="blocklist", path=path,
                    description="Blocklist data")


@blocklist.get()
def get_blocklist(request):
    prefix = request.matchdict['prefix']
    api_ver = int(request.matchdict['api_ver'])
    app = request.matchdict['application_guid']
    app_ver = request.matchdict['application_ver']

    # 1. Verify that we have a config for that prefix
    if prefix not in request.registry.amo_resources:
        raise HTTPNotFound()
    last_update = 0

    # Addons blocklist
    addons_records, addons_records_count = get_records(request, prefix, 'addons')
    if addons_records:
        last_update = addons_records[-1]['last_modified']

    # Plugins blocklist
    plugin_records, plugin_records_count = get_records(request, prefix, 'plugins')
    if plugin_records:
        last_update = max(last_update, plugin_records[-1]['last_modified'])

    # GFX blocklist
    gfx_records, gfx_records_count = get_records(request, prefix, 'gfx')
    if gfx_records:
        last_update = max(last_update, gfx_records[-1]['last_modified'])

    # Certificates blocklist
    cert_records, cert_records_count = get_records(request, prefix, 'certificates')
    if cert_records:
        last_update = max(last_update, cert_records[-1]['last_modified'])

    # Expose highest timestamp in response headers.
    last_etag = '"{}"'.format(last_update)
    request.response.headers['ETag'] = last_etag
    request.response.last_modified = last_update / 1000.0

    if_none_match = request.headers.get('If-None-Match')
    if_modified_since = request.headers.get('If-Modified-Since')
    if if_none_match is not None or if_modified_since is not None:
        has_changed = (if_none_match != last_etag and
                       request.if_modified_since != request.response.last_modified)
        if not has_changed:
            response = HTTPNotModified()
            response.headers['ETag'] = last_etag
            response.last_modified = last_update / 1000.0
            raise response

    xml_tree = etree.Element(
        'blocklist',
        xmlns="http://www.mozilla.org/2006/addons-blocklist",
        lastupdate='%s' % last_update
    )

    write_addons_items(xml_tree, addons_records, api_ver=api_ver, app_id=app, app_ver=app_ver)
    write_plugin_items(xml_tree, plugin_records, api_ver=api_ver,
                       app_id=app, app_ver=app_ver)
    write_gfx_items(xml_tree, gfx_records, api_ver=api_ver, app_id=app)
    write_cert_items(xml_tree, cert_records, api_ver=api_ver, app_id=app, app_ver=app_ver)

    doc = etree.ElementTree(xml_tree)
    request.response.content_type = "application/xml;charset=UTF-8"

    request.response.write(etree.tostring(
        doc,
        pretty_print=True,
        xml_declaration=True,
        encoding='UTF-8').decode('utf-8'))

    return request.response


def get_records(request, prefix, collection):
    resources = request.registry.amo_resources
    return request.registry.storage.get_all(
        collection_id="record",
        parent_id=PARENT_PATTERN.format(**resources[prefix][collection]),
        filters=[Filter('enabled', True, utils.COMPARISON.EQ)])
