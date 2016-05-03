import pytest
from pyramid.exceptions import ConfigurationError
from kinto_amo import utils


def test_resource_definition_format_fails_when_wrong():
    resource = 'blahbla/bla'

    with pytest.raises(ConfigurationError):
        utils.parse_resource(resource)
