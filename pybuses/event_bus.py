import typing
from collections import defaultdict

from pybuses.foundation import get_subscribed
from pybuses.types import (
    Listener,
    Subscribable,
)


class EventBus:

    def __init__(self) -> None:
        self._listeners: typing.Dict[Subscribable, typing.List[Listener]] = defaultdict(list)

    def subscribe(self, listener: Listener) -> None:
        event = get_subscribed(listener)
        self._listeners[event].append(listener)

    def post(self, event: Subscribable) -> None:
        event_class = type(event)
        if event_class not in self._listeners:
            return

        for listener in self._listeners[event_class]:
            listener(event)
