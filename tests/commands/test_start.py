import pytest
from click.testing import CliRunner

from cel.commands import start


def test_start_against_existing_folder_causes_a_non_zero_exit(tmpdir):
    with tmpdir.as_cwd():
        tmpdir.mkdir('test_cel')
        runner = CliRunner()
        result = runner.invoke(start.start, ['test_cel'])
    tmpdir.remove(rec=1)
    assert result.exit_code != 0


def test_creates_project_dir(tmpdir):
    with tmpdir.as_cwd():
        runner = CliRunner()
        result = runner.invoke(start.start, ['test_cel'])
    tmpdir.remove(rec=1)
    assert result.exit_code == 0


def test_creates_project_dir_when_exists_and_forced(tmpdir):
    with tmpdir.as_cwd():
        tmpdir.mkdir('test_cel')
        runner = CliRunner()
        result = runner.invoke(start.start, ['-f', 'test_cel'])
    tmpdir.remove(rec=1)
    assert result.exit_code == 0


def test_creates_config_file(tmpdir):
    with tmpdir.as_cwd():
        runner = CliRunner()
        runner.invoke(start.start, ['test_cel'])
    try:
        tmpdir.join('test_cel', 'cel.json').stat()
    except Exception:
        pytest.fail('config file does not exist')
    tmpdir.remove(rec=1)


def test_templates_lists_available_templates():
    runner = CliRunner()
    result = runner.invoke(start.templates)
    assert result.exit_code == 0
    assert 'default' in result.output
