import json
import os
import shutil
import sys

import click

from ..utils import get_root_dir, list_templates


@click.command()
@click.argument('name')
@click.option(
    '--force',
    '-f',
    is_flag=True,
    default=False,
    help='force cel to use an existing directory'
)
@click.option(
    '--template',
    '-t',
    type=click.Choice(list_templates()),
    default='default',
    help='What template to build from'
)
def start(name, force, template):
    """Start a new cel"""
    if os.path.exists(name):
        if not force:
            click.secho(f"The folder '{name}' already exists", fg='red')
            sys.exit(1)
    else:
        os.makedirs(name)

    template_dir = os.path.join(get_root_dir(), 'templates', template)

    for src_dir, dirs, files in os.walk(template_dir):
        dst_dir = src_dir.replace(template_dir, name, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            shutil.copy(src_file, dst_dir)

    config_path = os.path.join(name, 'cel.json')
    with open(config_path, 'w') as f:
        json.dump({
            "app": {
                "repository": "cel",
                "name": name
            }
        }, f, indent=2)


@click.command()
def templates():
    """List available templates"""
    click.secho("available templates:")
    for name in list_templates():
        click.secho("\t- {}".format(name), bold=True)
