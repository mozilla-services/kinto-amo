

def includeme(config):
    # Expose capability
    url = "https://github.com/mozilla-services/kinto-amo/"
    desc = "An endpoint to generate v2 and v3 XML blocklist export."
    config.add_api_capability("blocklist-xml", description=desc, url=url)
    config.scan('kinto_amo.views')
