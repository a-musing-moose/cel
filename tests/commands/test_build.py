import sys

from click.testing import CliRunner

from cel.commands import build
from cel.config import Config


def test_build_runner(monkeypatch):
    def mock_run(cmd, stdout):
        assert stdout == sys.stdout
        assert cmd == [
            'docker',
            'build',
            '-t',
            'cel/runner',
            '.',
        ]
    monkeypatch.setattr('cel.commands.build.run', mock_run)
    runner = CliRunner()
    result = runner.invoke(build.build_runner)
    assert result.exit_code == 0


def test_build(monkeypatch):
    def mock_run(cmd):
        assert cmd == [
            'docker',
            'build',
            '-t',
            'cel/test',
            '.'
        ]
    monkeypatch.setattr('cel.commands.build.run', mock_run)

    def mock_get_app_config():
        return Config('cel', 'test')
    monkeypatch.setattr('cel.commands.build.get_app_config', mock_get_app_config)

    runner = CliRunner()
    result = runner.invoke(build.build)
    assert result.exit_code == 0


def test_build_with_tag(monkeypatch):
    def mock_run(cmd):
        assert cmd == [
            'docker',
            'build',
            '-t',
            'cel/test:0.0.1',
            '.'
        ]
    monkeypatch.setattr('cel.commands.build.run', mock_run)

    def mock_get_app_config():
        return Config('cel', 'test')
    monkeypatch.setattr('cel.commands.build.get_app_config', mock_get_app_config)

    runner = CliRunner()
    result = runner.invoke(build.build, ['-t', '0.0.1'])
    assert result.exit_code == 0
    result = runner.invoke(build.build, ['--tag', '0.0.1'])
    assert result.exit_code == 0


def test_build_exits_when_inifile_not_found():
    runner = CliRunner()
    result = runner.invoke(build.build)
    assert result.exit_code == 1
