import typing
from unittest import mock

import pytest

from pybuses import EventBus
from pybuses.types import (
    Listener,
    Subscribable,
)


@pytest.fixture()
def event_bus() -> EventBus:
    return EventBus()


@pytest.fixture()
def event_class() -> Subscribable:
    return type('AnEvent')


def test_should_run_listener(event_bus: EventBus, event_class: Subscribable) -> None:
    a_mock = mock.Mock()

    def handler(event: event_class) -> None:  # type: ignore
        a_mock(event)

    event_bus.subscribe(handler)
    an_event = event_class()  # type: ignore
    event_bus.post(an_event)

    a_mock.assert_called_once_with(an_event)


def test_should_not_allow_adding_invalid_subscriber(
        event_bus: EventBus, event_class: Subscribable
) -> None:
    def invalid_handler(_event: event_class, _another_arg: int) -> None:  # type: ignore
        pass

    with pytest.raises(ValueError):
        event_bus.subscribe(invalid_handler)  # type: ignore
