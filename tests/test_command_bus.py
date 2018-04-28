import contextlib
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


def create_middleware_and_mock() -> typing.Tuple[typing.Callable, mock.Mock]:
    middleware_mock = mock.Mock()

    @contextlib.contextmanager
    def my_middleware(command: pycommand_bus.CommandType) -> typing.Generator:
        yield
        middleware_mock(command)

    return my_middleware, middleware_mock


def test_should_call_middleware(exemplary_command: typing.Type) -> None:
    middleware, middleware_mock = create_middleware_and_mock()

    command_bus = pycommand_bus.CommandBus([middleware])

    @exemplary_command.handler
    def handler(_command: pycommand_bus.CommandType) -> None:
        pass

    command = exemplary_command('wololo')
    command_bus.handle(command)

    middleware_mock.assert_called_once_with(command)


def test_should_call_whole_chain(exemplary_command: typing.Type) -> None:
    middleware_1, middleware_mock_1 = create_middleware_and_mock()
    middleware_2, middleware_mock_2 = create_middleware_and_mock()

    command_bus = pycommand_bus.CommandBus([middleware_1, middleware_2])

    @exemplary_command.handler
    def handler(_command: pycommand_bus.CommandType) -> None:
        pass

    command = exemplary_command('wololo')
    command_bus.handle(command)

    middleware_mock_1.assert_called_once_with(command)
    middleware_mock_2.assert_called_once_with(command)
