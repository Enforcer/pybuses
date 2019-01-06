import contextlib
import typing
from unittest import mock

import pytest

import pybuses


@pytest.fixture()
def command_bus() -> pybuses.CommandBus:
    return pybuses.CommandBus()


def test_should_execute_command(command_bus: pybuses.CommandBus, exemplary_command: typing.Type) -> None:
    a_mock = mock.Mock()

    def handler(command: exemplary_command) -> None:  # type: ignore
        a_mock(command)

    command_bus.subscribe(handler)

    command = exemplary_command('some_data')
    command_bus.handle(command)

    a_mock.assert_called_once_with(command)


def test_should_raise_exception_if_handler_has_not_been_registered(
    command_bus: pybuses.CommandBus, exemplary_command: typing.Type
) -> None:
    command = exemplary_command('czy ta bajka sie nie konczy zleeeee')

    with pytest.raises(Exception):
        command_bus.handle(command)


def test_should_not_allow_for_multiple_handlers(
    command_bus: pybuses.CommandBus, exemplary_command: typing.Type
) -> None:
    def handler(_command: exemplary_command) -> None:  # type: ignore
        pass

    command_bus.subscribe(handler)

    with pytest.raises(Exception):
        command_bus.subscribe(handler)


def create_middleware_and_mock() -> typing.Tuple[typing.Callable, mock.Mock]:
    middleware_mock = mock.Mock()

    @contextlib.contextmanager
    def my_middleware(command) -> typing.Generator:  # type: ignore
        yield
        middleware_mock(command)

    return my_middleware, middleware_mock


def test_should_call_middleware(exemplary_command: typing.Type) -> None:
    middleware, middleware_mock = create_middleware_and_mock()

    command_bus = pybuses.CommandBus([middleware])

    def handler(_command: exemplary_command) -> None:    # type: ignore
        pass

    command_bus.subscribe(handler)

    command = exemplary_command('wololo')
    command_bus.handle(command)

    middleware_mock.assert_called_once_with(command)


def test_should_call_whole_chain(exemplary_command: typing.Type) -> None:
    middleware_1, middleware_mock_1 = create_middleware_and_mock()
    middleware_2, middleware_mock_2 = create_middleware_and_mock()

    command_bus = pybuses.CommandBus([middleware_1, middleware_2])

    def handler(_command: exemplary_command) -> None:    # type: ignore
        pass

    command_bus.subscribe(handler)
    command = exemplary_command('wololo')
    command_bus.handle(command)

    middleware_mock_1.assert_called_once_with(command)
    middleware_mock_2.assert_called_once_with(command)
