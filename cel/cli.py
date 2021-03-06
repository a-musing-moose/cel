import click

from .commands.build import build, build_runner
from .commands.run import run
from .commands.start import start, templates


@click.group()
def main():  # pragma: nocover
    pass


main.add_command(build)
main.add_command(build_runner)
main.add_command(run)
main.add_command(start)
main.add_command(templates)
