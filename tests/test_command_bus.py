import typing
from unittest import mock

import pytest

from pycommand_bus import (
    CommandBus,
    command,
)


@pytest.fixture()
def command_bus() -> CommandBus:
    return CommandBus()


@pytest.fixture()
def exemplary_command() -> typing.Type:
    @command
    class Example:
        def __init__(self, data) -> None:
            self.data = data

        def __repr__(self):
            return '<{} data={}>'.format(self.__class__.__name__, self.data)

    return Example


def test_should_execute_command(command_bus: CommandBus, exemplary_command: typing.Type) -> None:
    handler_mock = mock.Mock()
    exemplary_command.handler(handler_mock)

    command = exemplary_command('some_data')
    bus = CommandBus().dispatch(command)

    handler_mock.assert_called_once_with(command)


def test_should_raise_exception_if_handler_has_not_been_registered(
    command_bus: CommandBus, exemplary_command: typing.Type
) -> None:
    command = exemplary_command('czy ta bajka sie nie konczy zleeeee')

    with pytest.raises(Exception):
        command_bus.dispatch(command)


def test_should_not_allow_for_registering_multiple_handlers(exemplary_command: typing.Type):
    exemplary_command.handler(lambda: None)

    with pytest.raises(Exception):
        exemplary_command.handler(lambda: None)
