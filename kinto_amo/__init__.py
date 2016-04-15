

def includeme(config):
    # # Expose capability.
    config.add_api_capability("amo",
                              description="AMO-style API for Kinto",
                              url="https://github.com/mozilla-services/kinto-amo/")


    config.scan('kinto_amo.views')
