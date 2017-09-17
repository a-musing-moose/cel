import configparser
import os

from .exceptions import ConfigNotFound


class Config(object):

    def __init__(self, repository, name):
        self.repository = repository
        self.name = name

    @property
    def image_name(self):
        return f'{self.repository}/{self.name}'

    @classmethod
    def from_ini(cls, path):
        if not os.path.exists(path):
            raise ConfigNotFound()

        config = configparser.ConfigParser()
        config.read(path)

        repository = config['app']['repository']
        name = config['app']['name']
        return cls(repository, name)
