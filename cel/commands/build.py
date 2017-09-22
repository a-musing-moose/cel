import os
import sys
from subprocess import run

import click

from ..utils import get_app_config, get_root_dir


@click.command()
@click.option('--tag', '-t', default=None, help='add an optional tag to the build')
def build(tag):
    """Build your cel"""
    config = get_app_config()
    image_name = config.image_name
    if tag:
        image_name = f'{image_name}:{tag}'
    cmd = [
        'docker',
        'build',
        '-t',
        image_name,
        '.'
    ]
    run(cmd)


@click.command()
def build_runner():
    """Build the base runner"""
    docker_dir = os.path.join(get_root_dir(), 'runner')
    current = os.getcwd()
    os.chdir(docker_dir)
    cmd = [
        'docker',
        'build',
        '-t',
        'cel/runner',
        '.',
    ]
    run(cmd, stdout=sys.stdout)
    os.chdir(current)  # ensure we switch back to previous directory
