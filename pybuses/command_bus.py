import contextlib
import typing

from pybuses.foundation import get_subscribed
from pybuses.types import (
    Subscribable,
    Listener,
)


class CommandBus:
    def __init__(self, middlewares: typing.Optional[typing.List[typing.Callable]] = None) -> None:
        if not middlewares:
            middlewares = []

        self._middlewares = middlewares
        self._handlers: typing.Dict[Subscribable, Listener] = {}

    def subscribe(self, listener: Listener) -> None:
        command = get_subscribed(listener)
        if command in self._handlers:
            raise ValueError('{} already has a handler ({})!'.format(command, self._handlers[command]))
        self._handlers[command] = listener

    def handle(self, command: Subscribable) -> None:
        try:
            handler = self._handlers[type(command)]
        except KeyError:
            raise Exception('No handler for {!r}'.format(command))

        with contextlib.ExitStack() as stack:
            for middleware in self._middlewares:
                stack.enter_context(middleware(command))
            handler(command)
