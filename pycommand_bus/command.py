import weakref

from pycommand_bus import constants


def command(class_):
    def add_handler_decorator(func):
        attr_name = '_pycommand_bus_handler'
        if hasattr(class_, attr_name):
            raise Exception('You can use only one handler for each command!')

        setattr(class_, constants.HANDLER_ATTR_NAME, weakref.ref(func))

    setattr(class_, 'handler', add_handler_decorator)
    return class_
