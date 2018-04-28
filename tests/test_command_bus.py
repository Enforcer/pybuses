import typing
from collections import namedtuple
from unittest import mock

import pytest

from pycommand_bus import (
    command,
    command_bus,
)


@pytest.fixture()
def exemplary_command() -> typing.Type:
    @command
    class Example:
        def __init__(self, data: str) -> None:
            self.data = data

        def __repr__(self) -> str:
            return '<{} data={}>'.format(self.__class__.__name__, self.data)

    return Example


def test_should_execute_command(exemplary_command: typing.Type) -> None:
    handler_mock = mock.Mock()
    exemplary_command.handler(handler_mock)

    command = exemplary_command('some_data')
    command_bus.dispatch(command)

    handler_mock.assert_called_once_with(command)


def test_should_raise_exception_if_handler_has_not_been_registered(
    exemplary_command: typing.Type
) -> None:
    command = exemplary_command('czy ta bajka sie nie konczy zleeeee')

    with pytest.raises(Exception):
        command_bus.dispatch(command)


def test_should_not_allow_for_registering_multiple_handlers(exemplary_command: typing.Type) -> None:
    exemplary_command.handler(lambda: None)

    with pytest.raises(Exception):
        exemplary_command.handler(lambda: None)


@pytest.mark.parametrize('command', [
    namedtuple('Example', 'field_a field_b'),
    type('Example', (), {'__slots__': ()})
])
def should_raise_exception_if_can_not_set_handler(command: object) -> None:
    with pytest.raises(Exception):
        exemplary_command.handler(lambda: None)
