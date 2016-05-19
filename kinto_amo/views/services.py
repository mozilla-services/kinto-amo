from kinto.core import Service, utils
from kinto.core.storage import Filter

from amo2kinto.exporter import (
    write_addons_items, write_plugin_items, write_gfx_items, write_cert_items
)
from lxml import etree

path = ('/blocklist/{api_ver:\d+}/{application_guid}/{application_ver}/'
        '{metrics:.*}')

PARENT_PATTERN = "/buckets/{bucket}/collections/{collection}"

blocklist = Service(name="blocklist", path=path,
                    description="Blocklist data")


@blocklist.get()
def get_blocklist(request):
    api_ver = int(request.matchdict['api_ver'])
    app = request.matchdict['application_guid']
    app_ver = request.matchdict['application_ver']

    last_update = 0

    # Addons blocklist
    addons_records, addons_records_count = get_records(request, 'addons')
    if addons_records:
        last_update = addons_records[-1]['last_modified']

    # Plugins blocklist
    plugin_records, plugin_records_count = get_records(request, 'plugins')
    if plugin_records:
        last_update = max(last_update, plugin_records[-1]['last_modified'])

    # GFX blocklist
    gfx_records, gfx_records_count = get_records(request, 'gfx')
    if gfx_records:
        last_update = max(last_update, gfx_records[-1]['last_modified'])

    # Certificates blocklist
    cert_records, cert_records_count = get_records(request, 'certificates')
    if cert_records:
        last_update = max(last_update, cert_records[-1]['last_modified'])

    xml_tree = etree.Element(
        'blocklist',
        xmlns="http://www.mozilla.org/2006/addons-blocklist",
        lastupdate='%s' % last_update
    )

    write_addons_items(xml_tree, addons_records, api_ver=api_ver, app_id=app)
    write_plugin_items(xml_tree, plugin_records, api_ver=api_ver,
                       app_id=app, app_ver=app_ver)
    write_gfx_items(xml_tree, gfx_records, api_ver=api_ver, app_id=app)
    write_cert_items(xml_tree, cert_records, api_ver=api_ver)

    doc = etree.ElementTree(xml_tree)
    request.response.content_type = "application/xml;charset=UTF-8"

    request.response.write(etree.tostring(
        doc,
        pretty_print=True,
        xml_declaration=True,
        encoding='UTF-8').decode('utf-8'))

    return request.response


def get_records(request, collection):
    resources = request.registry.amo_resources
    return request.registry.storage.get_all(
        collection_id="record",
        parent_id=PARENT_PATTERN.format(**resources[collection]),
        filters=[Filter('enabled', True, utils.COMPARISON.EQ)])
