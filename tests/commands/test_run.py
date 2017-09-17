import subprocess
import sys
from unittest.mock import Mock

import click
from click.testing import CliRunner

from cel.commands import run
from cel.config import Config


def test_run(monkeypatch):

    @click.command()
    def mock_build():
        pass
    monkeypatch.setattr('cel.commands.run.build', mock_build)

    def mock_popen(cmd, stdin, stdout, stderr):
        assert cmd == [
            'docker',
            'run',
            '-i',
            '--rm',
            'cel/test'
        ]
        assert stdin == subprocess.PIPE
        assert stdout == sys.stdout
        assert stderr == sys.stderr
        m = Mock()
        m.communicate = Mock(return_value=('', ''))
        return m

    monkeypatch.setattr('cel.commands.run.subprocess.Popen', mock_popen)

    def mock_get_app_config():
        return Config('cel', 'test')
    monkeypatch.setattr('cel.commands.run.get_app_config', mock_get_app_config)

    runner = CliRunner()
    result = runner.invoke(run.run)
    assert result.exit_code == 0
