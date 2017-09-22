import json

import pytest

from cel.config import Config


@pytest.fixture()
def config():
    """A fixture that returns a config instance"""
    return Config('test_repo', 'test_name')


@pytest.fixture()
def config_file(tmpdir):
    """A fixture that writes a config file, and cleans up afterward"""
    directory = tmpdir.mkdir('test_folder')
    with directory.as_cwd():
        f = directory.join('cel.json')
        f.write(
            json.dumps({
                "app": {
                    "repository": "test_repo",
                    "name": "test_name"
                }
            })
        )
        yield str(f)
    directory.remove(rec=1)
