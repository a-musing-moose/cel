import os
import sys

from .config import Config
from .exceptions import ConfigNotFound


def get_root_dir():
    return os.path.dirname(__file__)


def list_templates():
    template_dir = os.path.join(get_root_dir(), 'templates')
    return [name for name in os.listdir(template_dir) if os.path.isdir(os.path.join(template_dir, name))]


def get_app_config():
    try:
        return Config.from_ini('config.ini')
    except ConfigNotFound:
        print("Cannot locate application config.ini")
        sys.exit(1)
