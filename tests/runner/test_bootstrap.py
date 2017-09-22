import json
from io import StringIO

import pytest

from cel.runner import bootstrap


def test_timeout_exits_with_none_zero_code():
    with pytest.raises(SystemExit) as e:
        bootstrap.timeout(None, None)

    assert e.value.code != 0


def test_timeout_outputs_an_json_error_message(capsys):
    capsys.readouterr()
    with pytest.raises(SystemExit):
        bootstrap.timeout(None, None)
    out, err = capsys.readouterr()
    assert 'error' in out
    assert 'error' in json.loads(out)


def test_missing_module_exits_with_none_zero_code():
    with pytest.raises(SystemExit) as e:
        bootstrap.get_entry_point()

    assert e.value.code != 0


def test_missing_module_outputs_an_json_error_message(capsys):
    capsys.readouterr()
    with pytest.raises(SystemExit):
        bootstrap.get_entry_point()
    out, err = capsys.readouterr()
    assert 'error' in out
    assert 'error' in json.loads(out)


def test_missing_entry_point_exits_with_none_zero_code(tmpdir, monkeypatch):
    app = tmpdir.join('app.py')
    app.write('pass')
    init = tmpdir.join('__init__.py')
    init.write('')
    monkeypatch.syspath_prepend(tmpdir)
    with pytest.raises(SystemExit) as e:
        bootstrap.get_entry_point()
    tmpdir.remove(rec=1)
    assert e.value.code != 0


def test_missing_entry_point_returns_error_json(tmpdir, monkeypatch, capsys):
    app = tmpdir.join('app.py')
    app.write('pass')
    init = tmpdir.join('__init__.py')
    init.write('')
    monkeypatch.syspath_prepend(tmpdir)
    capsys.readouterr()
    with pytest.raises(SystemExit):
        bootstrap.get_entry_point()
    tmpdir.remove(rec=1)
    out, err = capsys.readouterr()
    assert 'error' in out
    assert 'error' in json.loads(out)


def test_run_exits_if_stdin_not_json(monkeypatch, capsys):
    monkeypatch.setattr('cel.runner.bootstrap.get_entry_point', lambda: None)
    monkeypatch.setattr('cel.runner.bootstrap.sys.stdin', StringIO('{'))

    capsys.readouterr()
    with pytest.raises(SystemExit) as e:
        bootstrap.run()
    out, err = capsys.readouterr()

    assert e.value.code != 0
    assert 'error' in out
    assert 'error' in json.loads(out)


def test_entry_point_exception_causes_exit(monkeypatch, capsys):
    expected_message = 'test exception'

    def mock_entry(payload):
        raise Exception(expected_message)

    monkeypatch.setattr('cel.runner.bootstrap.get_entry_point', lambda: mock_entry)
    monkeypatch.setattr('cel.runner.bootstrap.sys.stdin', StringIO('{}'))

    capsys.readouterr()
    with pytest.raises(SystemExit) as e:
        bootstrap.run()
    out, err = capsys.readouterr()

    assert e.value.code != 0
    assert 'error' in out
    data = json.loads(out)
    assert 'error' in data
    assert data['error'] == expected_message


def test_successful_run_exits_with_a_zero(monkeypatch, capsys):
    expected_response = {
        'success': True
    }

    def mock_entry(payload):
        return expected_response

    monkeypatch.setattr('cel.runner.bootstrap.get_entry_point', lambda: mock_entry)
    monkeypatch.setattr('cel.runner.bootstrap.sys.stdin', StringIO('{}'))

    capsys.readouterr()
    with pytest.raises(SystemExit) as e:
        bootstrap.run()
    out, err = capsys.readouterr()

    assert e.value.code == 0
    data = json.loads(out)
    assert data == expected_response
