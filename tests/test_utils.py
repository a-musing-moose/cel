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


def test_config_loading(tmpdir):
    directory = tmpdir.mkdir('testing')
    old_dir = directory.chdir()
    f = directory.join('config.ini')
    f.write((
        '[app]\n'
        'repository=cel\n'
        'name=app_name'
    ))
    config = utils.get_app_config()
    old_dir.chdir()
    assert config.repository == 'cel'
    assert config.name == 'app_name'


def test_config_load_when_file_not_present():
    with pytest.raises(SystemExit) as e:
        utils.get_app_config()
        assert e.value.code != 0
