import json

import pytest

from cel import config
from cel.exceptions import ConfigNotFound, ConfigSyntaxError


def test_image_name_property():
    repository = 'repo'
    name = 'test-name'
    instance = config.Config(repository, name)
    assert instance.image_name == f'{repository}/{name}'


def test_loading_from_file(tmpdir):
    test_dir = tmpdir.mkdir('testing')
    f = test_dir.join('cel.json')
    f.write(
        json.dumps({
            "app": {
                "repository": "cel",
                "name": "app_name"
            }
        })
    )
    instance = config.Config.from_file(str(f))
    assert instance.image_name == 'cel/app_name'


def test_loading_from_file_raises_exception_when_file_content_cannot_be_parsed(tmpdir):
    test_dir = tmpdir.mkdir('testing')
    f = test_dir.join('cel.json')
    f.write('{')
    with pytest.raises(ConfigSyntaxError):
        config.Config.from_file(str(f))


def test_loading_from_dict_sets_defaults():
    settings = config.Config.from_dict({})
    assert settings.repository == config.DEFAULT_SETTINGS['app']['repository']
    assert settings.name == config.DEFAULT_SETTINGS['app']['name']


def test_loading_from_dict_does_not_override_passed_in_values():
    settings = config.Config.from_dict({
        'app': {
            'repository': 'test',
            'name': 'name'
        }
    })
    assert settings.repository == 'test'
    assert settings.name == 'name'


def test_loading_from_file_raises_exception_if_file_not_found():
    with pytest.raises(ConfigNotFound):
        config.Config.from_file("i_dont_exist.ini")
