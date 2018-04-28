import typing
import weakref

from pycommand_bus import constants


CommandCandidateType = typing.TypeVar('CommandCandidateType')


ADD_HANDLER_DECORATOR_PROP_NAME = 'handler'


class CommandType:
    @classmethod
    def handler(self, fun: typing.Callable) -> typing.Callable:
        pass


def command(class_: CommandCandidateType) -> typing.Union[CommandCandidateType, CommandType]:
    def _add_handler_decorator(func: typing.Callable) -> None:
        attr_name = '_pycommand_bus_handler'
        if hasattr(class_, attr_name):
            raise Exception('You can use only one handler for each command!')

        setattr(class_, constants.HANDLER_ATTR_NAME, weakref.ref(func))

    try:
        setattr(class_, 'handler', _add_handler_decorator)
    except AttributeError:
        raise Exception('Can not set handler')
    return class_
