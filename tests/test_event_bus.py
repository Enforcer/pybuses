import typing
from unittest import mock

import pytest

from pycommand_bus import (
    EventBus,
    types,
)


@pytest.fixture()
def event_bus() -> EventBus:
    return EventBus()


@pytest.fixture()
def event_class() -> typing.Type[types.EventType]:
    class AnEvent:
        pass

    return AnEvent


def test_should_run_listener(event_bus: EventBus, event_class: typing.Type[types.EventType]) -> None:
    a_mock = mock.Mock()
    def handler(event: event_class) -> None:
        a_mock(event)

    event_bus.register(handler)
    an_event = event_class()
    event_bus.post(an_event)

    a_mock.assert_called_once_with(an_event)
