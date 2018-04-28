import typing

from pycommand_bus import (
    command_decorator,
    constants,
    middleware as pycommand_bus_middleware,
)


class CommandBus:
    def __init__(self, middlewares: typing.Optional[typing.List[pycommand_bus_middleware.Middleware]] = None) -> None:
        if not middlewares:
            middlewares = []

        if not all(isinstance(middleware, pycommand_bus_middleware.Middleware) for middleware in middlewares):
            raise Exception(
                'All middlewares must be instances of {}'.format(pycommand_bus_middleware.Middleware.__name__)
            )

        self._middlewares = middlewares

    def handle(self, command: command_decorator.CommandType) -> None:
        try:
            handler_weak_ref = getattr(command, constants.HANDLER_ATTR_NAME)
            handler = handler_weak_ref()
        except (AttributeError, TypeError):
            raise Exception('No handler for {!r}'.format(command))

        assert callable(handler)
        for middleware in self._middlewares:
            middleware.before(command)
        handler(command)
        for middleware in self._middlewares:
            middleware.after(command)
