import contextlib
import typing

from pycommand_bus import (
    decorators,
    constants,
)


class CommandBus:
    def __init__(self, middlewares: typing.Optional[typing.List[typing.Callable]] = None) -> None:
        if not middlewares:
            middlewares = []

        self._middlewares = middlewares

    def handle(self, command: decorators.CommandType) -> None:
        try:
            handler_weak_ref = getattr(command, constants.HANDLER_ATTR_NAME)
            handler = handler_weak_ref()
        except (AttributeError, TypeError):
            raise Exception('No handler for {!r}'.format(command))

        with contextlib.ExitStack() as stack:
            for middleware in self._middlewares:
                stack.enter_context(middleware(command))
            handler(command)
