from pyramid.exceptions import ConfigurationError

ERROR_MSG = ("Resources should be defined as "
             "'/buckets/<bid>/collections/<cid>'. Got %r")


def parse_resource(resource):
    parts = resource.split('/')
    if len(parts) == 5:
        _, _, bucket, _, collection = parts
    else:
        raise ConfigurationError(ERROR_MSG % resource)
    return {
        'bucket': bucket,
        'collection': collection
    }
