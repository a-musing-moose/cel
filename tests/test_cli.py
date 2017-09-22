from cel import cli


def test_main_has_all_commands_registered():
    for command in ['build', 'build_runner', 'start', 'run', 'templates']:
        assert command in cli.main.commands
