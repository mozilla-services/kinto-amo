import pkg_resources

#: Module version, as defined in PEP-0396.
__version__ = pkg_resources.get_distribution(__package__).version


def includeme(config):
    resources = {
        "blocklist": {
            "addons": {"bucket": "blocklists", "collection": "addons"},
            "plugins": {"bucket": "blocklists", "collection": "plugins"},
            "gfx": {"bucket": "blocklists", "collection": "gfx"},
            "certificates": {"bucket": "blocklists", "collection": "certificates"},
        },
        "preview": {
            "addons": {"bucket": "blocklists-preview", "collection": "addons"},
            "certificates": {
                "bucket": "blocklists-preview",
                "collection": "certificates",
            },
            "gfx": {"bucket": "blocklists-preview", "collection": "gfx"},
            "plugins": {"bucket": "blocklists-preview", "collection": "plugins"},
        },
    }
    config.registry.amo_resources = resources

    # Expose capability
    url = "https://github.com/mozilla-services/kinto-amo/"
    desc = "An endpoint to generate v2 and v3 XML blocklist export."
    config.add_api_capability(
        "blocklist-xml",
        version=__version__,
        description=desc,
        url=url,
        resources=resources,
    )

    config.scan("kinto_amo.views")
