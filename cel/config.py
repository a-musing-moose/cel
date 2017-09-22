import json
import os

from .exceptions import ConfigNotFound, ConfigSyntaxError


DEFAULT_SETTINGS = {
    "app": {
        "repository": "cel",
        "name": None,
    }
}


def merge_dicts(destination, source):
    """Recursively merge one dict into another"""
    for k, v in source.items():
        if k in destination and isinstance(destination[k], dict) and isinstance(source[k], dict):
            merge_dicts(destination[k], source[k])
        elif source[k] is not None:
            destination[k] = source[k]


class Config(object):

    def __init__(self, repository, name, **kwargs):
        self.repository = repository
        self.name = name
        self.kwargs = kwargs

    @property
    def image_name(self):
        return f'{self.repository}/{self.name}'

    @classmethod
    def from_dict(cls, settings):
        data = DEFAULT_SETTINGS.copy()
        merge_dicts(data, settings)
        app_settings = data.pop("app")

        return cls(app_settings['repository'], app_settings['name'], **data)

    @classmethod
    def from_file(cls, path):
        if not os.path.exists(path):
            raise ConfigNotFound()

        with open(path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ConfigSyntaxError(str(e))

        return cls.from_dict(data)
