from pycommand_bus import (
    command_decorator,
    constants,
)


def handle(command: command_decorator.CommandType) -> None:
    try:
        handler_weak_ref = getattr(command, constants.HANDLER_ATTR_NAME)
        handler = handler_weak_ref()
    except (AttributeError, TypeError):
        raise Exception('No handler for {!r}'.format(command))

    handler(command)
