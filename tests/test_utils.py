import os

import pytest

from cel import utils


def test_get_root_dir():
    assert utils.get_root_dir() == os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'cel'
        )
    )


def test_list_templates():
    assert utils.list_templates() == ['default']


def test_config_loading(config_file):
    config = utils.get_app_config()
    assert config.repository == 'test_repo'
    assert config.name == 'test_name'


def test_config_load_when_file_not_present():
    with pytest.raises(SystemExit) as e:
        utils.get_app_config()
        assert e.value.code != 0
