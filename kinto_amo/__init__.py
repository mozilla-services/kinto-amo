import pkg_resources
from collections import OrderedDict
from pyramid.exceptions import ConfigurationError
from .utils import parse_resource

#: Module version, as defined in PEP-0396.
__version__ = pkg_resources.get_distribution(__package__).version

DEFAULT_ADDONS = '/buckets/blocklists/collections/addons'
DEFAULT_PLUGINS = '/buckets/blocklists/collections/plugins'
DEFAULT_GFX = '/buckets/blocklists/collections/gfx'
DEFAULT_CERTIFICATES = '/buckets/blocklists/collections/certificates'


def includeme(config):
    # Parse resources
    settings = config.get_settings()
    resources = OrderedDict()

    # Configure default settings
    # We are using an OrderedDict to always present the resource in
    # the same order in the capability page, it also helps for tests.
    resources['blocklist'] = OrderedDict()
    resources['blocklist']['addons'] = parse_resource(DEFAULT_ADDONS)
    resources['blocklist']['plugins'] = parse_resource(DEFAULT_PLUGINS)
    resources['blocklist']['gfx'] = parse_resource(DEFAULT_GFX)
    resources['blocklist']['certificates'] = parse_resource(DEFAULT_CERTIFICATES)

    # Read blocklist settings
    for settings_key, settings_value in settings.items():
        if not settings_key.startswith('amo.'):
            continue
        parts = settings_key.split('.', 3)

        if len(parts) == 2:  # amo.addons
            prefix = 'blocklist'
            _, blocklist = parts
        else:  # amo.preview.addons
            _, prefix, blocklist = parts

        resource = resources.setdefault(prefix, OrderedDict())
        resource[blocklist] = parse_resource(settings_value)

    for resource in resources.values():
        inter = set(resource.keys()) & {'addons', 'plugins', 'gfx', 'certificates'}
        if len(inter) != 4:
            raise ConfigurationError("Incomplete blocklist configuration: %s" % inter)

    config.registry.amo_resources = resources

    # Expose capability
    url = "https://github.com/mozilla-services/kinto-amo/"
    desc = "An endpoint to generate v2 and v3 XML blocklist export."
    config.add_api_capability("blocklist-xml", version=__version__,
                              description=desc, url=url, resources=resources)

    config.scan('kinto_amo.views')
