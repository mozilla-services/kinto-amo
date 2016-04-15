

def includeme(config):
    # Expose capability
    url = "https://github.com/mozilla-services/kinto-amo/"
    desc = "AMO-style API for Kinto"
    config.add_api_capability("amo", description=desc, url=url)
    config.scan('kinto_amo.views')
