import subprocess
import sys
from unittest.mock import Mock

import click
from click.testing import CliRunner

from cel.commands import run


def test_run(monkeypatch, config):

    monkeypatch.setattr('cel.commands.run.build', click.command()(lambda: None))

    def mock_popen(cmd, stdin, stdout, stderr):
        assert cmd == [
            'docker',
            'run',
            '-i',
            '--rm',
            'test_repo/test_name'
        ]
        assert stdin == subprocess.PIPE
        assert stdout == sys.stdout
        assert stderr == sys.stderr
        m = Mock()
        m.communicate = Mock(return_value=('', ''))
        return m

    monkeypatch.setattr('cel.commands.run.subprocess.Popen', mock_popen)
    monkeypatch.setattr('cel.commands.run.get_app_config', lambda: config)

    runner = CliRunner()
    result = runner.invoke(run.run)
    assert result.exit_code == 0


def test_invalid_json_file_causes_non_zero_exit(monkeypatch, tmpdir):
    json_file = tmpdir.join('some.json')
    json_file.write('{')

    monkeypatch.setattr('cel.commands.run.build', click.command()(lambda: None))

    runner = CliRunner()
    result = runner.invoke(run.run, ['-f', str(json_file)])
    json_file.remove()
    assert result.exit_code != 0


def test_invalid_json_body_causes_non_zero_exit(monkeypatch):
    monkeypatch.setattr('cel.commands.run.build', click.command()(lambda: None))

    runner = CliRunner()
    result = runner.invoke(run.run, ['-b', '{'])
    assert result.exit_code != 0


def test_run_passes_through_additional_args(monkeypatch, config):

    monkeypatch.setattr('cel.commands.run.build', click.command()(lambda: None))
    comms = Mock(return_value=('', ''))

    def mock_popen(cmd, stdin, stdout, stderr):
        m = Mock()
        m.communicate = comms
        return m

    monkeypatch.setattr('cel.commands.run.subprocess.Popen', mock_popen)
    monkeypatch.setattr('cel.commands.run.get_app_config', lambda: config)

    runner = CliRunner()
    runner.invoke(run.run, ['other', 'params'])
    comms.assert_called_with(input=b'{"argv": ["other", "params"]}')
