from pycommand_bus import (
    command,
    constants,
)


def handle(command: object) -> None:
    try:
        handler_weak_ref = getattr(command, constants.HANDLER_ATTR_NAME)
        handler = handler_weak_ref()
    except (AttributeError, TypeError):
        raise Exception('No handler for {!r}'.format(command))

    handler(command)
