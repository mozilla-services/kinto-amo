from collections import OrderedDict
from .utils import parse_resource

DEFAULT_ADDONS = '/buckets/blocklists/collections/addons'
DEFAULT_PLUGINS = '/buckets/blocklists/collections/plugins'
DEFAULT_GFX = '/buckets/blocklists/collections/gfx'
DEFAULT_CERTIFICATES = '/buckets/blocklists/collections/certificates'


def includeme(config):
    # Parse resources
    settings = config.get_settings()
    resources = OrderedDict()
    resources['addons'] = parse_resource(
        settings.get('amo.addons', DEFAULT_ADDONS))
    resources['plugins'] = parse_resource(
        settings.get('amo.plugins', DEFAULT_PLUGINS))
    resources['gfx'] = parse_resource(
        settings.get('amo.gfx', DEFAULT_GFX))
    resources['certificates'] = parse_resource(
        settings.get('amo.certificates', DEFAULT_CERTIFICATES))

    config.registry.amo_resources = resources

    # Expose capability
    url = "https://github.com/mozilla-services/kinto-amo/"
    desc = "An endpoint to generate v2 and v3 XML blocklist export."
    config.add_api_capability("blocklist-xml",
                              description=desc, url=url, resources=resources)

    config.scan('kinto_amo.views')
