import typing
import collections

import pytest


def test_should_not_allow_for_registering_multiple_handlers(exemplary_command: typing.Type) -> None:
    exemplary_command.handler(lambda: None)

    with pytest.raises(Exception):
        exemplary_command.handler(lambda: None)


def test_should_raise_exception_if_handler_is_not_callable(exemplary_command: typing.Type) -> None:
    NotCallableObject = type('NotCallableObject', (), {})

    with pytest.raises(Exception):
        exemplary_command.handler(NotCallableObject())


@pytest.mark.parametrize('command', [
    collections.namedtuple('Example', 'field_a field_b'),
    type('Example', (), {'__slots__': ()})
])
def test_should_raise_exception_if_can_not_set_handler(command: typing.Type) -> None:
    with pytest.raises(Exception):
        command.handler(lambda: None)
