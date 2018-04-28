import typing
from unittest import mock

import pytest

from pycommand_bus import command_bus


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
