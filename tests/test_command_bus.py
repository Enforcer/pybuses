import typing
from unittest import mock

import pytest

import pycommand_bus


@pytest.fixture()
def command_bus() -> pycommand_bus.CommandBus:
    return pycommand_bus.CommandBus()


def test_should_execute_command(command_bus: pycommand_bus.CommandBus, exemplary_command: typing.Type) -> None:
    handler_mock = mock.Mock()
    exemplary_command.handler(handler_mock)

    command = exemplary_command('some_data')
    command_bus.handle(command)

    handler_mock.assert_called_once_with(command)


def test_should_raise_exception_if_handler_has_not_been_registered(
    command_bus: pycommand_bus.CommandBus, exemplary_command: typing.Type
) -> None:
    command = exemplary_command('czy ta bajka sie nie konczy zleeeee')

    with pytest.raises(Exception):
        command_bus.handle(command)


def test_should_call_middleware(exemplary_command: typing.Type) -> None:
    middleware_mock = mock.Mock()
    command_bus = pycommand_bus.CommandBus([middleware_mock])
    handler_mock = mock.Mock()
    exemplary_command.handler(handler_mock)

    command = exemplary_command('wololo')
    command_bus.handle(command)

    middleware_mock.assert_called_once_with(command)
