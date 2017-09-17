import pytest

from cel import config
from cel.exceptions import ConfigNotFound


def test_image_name_property():
    repository = 'repo'
    name = 'test-name'
    instance = config.Config(repository, name)
    assert instance.image_name == f'{repository}/{name}'


def test_loading_from_ini(tmpdir):
    test_dir = tmpdir.mkdir('testing')
    f = test_dir.join('config.ini')
    f.write((
        '[app]\n'
        'repository=cel\n'
        'name=app_name'
    ))
    instance = config.Config.from_ini(str(f))
    assert instance.image_name == 'cel/app_name'


def test_loading_from_ini_raises_exception_if_file_not_found():
    with pytest.raises(ConfigNotFound):
        config.Config.from_ini("i_dont_exist.ini")
