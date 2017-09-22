import json
import subprocess
import sys

import click

from ..utils import get_app_config
from .build import build


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.option('--file', '-f', type=click.File(), help='a file containing the json payload')
@click.option('--body', '-b', help='a string containing the json payload')
@click.option('--no-build', is_flag=True, default=False, help='do not rebuild the app before running')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def run(ctx, file, body, no_build, args):
    """Run a cel locally"""
    if not no_build:
        ctx.invoke(build)
    payload = {}
    if file:
        try:
            payload = json.load(file)
        except json.JSONDecodeError:
            click.secho("That is not a valid JSON file", fg='red')
            sys.exit(1)

    if body:
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            click.secho(f"{body} is not a valid JSON string", fg='red')
            sys.exit(1)

    if args:
        payload['argv'] = args

    config = get_app_config()
    cmd = [
        'docker',
        'run',
        '-i',
        '--rm',
        config.image_name
    ]
    p = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    p.communicate(input=json.dumps(payload).encode('utf8'))
