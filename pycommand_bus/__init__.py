import weakref

from pycommand_bus.command_bus import CommandBus


def command(class_):
    def add_handler_decorator(func):
        attr_name = '_pycommand_bus_handler'
        if getattr(class_, attr_name, None):
            raise Exception('You can use only one handler for each command!')

        class_._pycommand_bus_handler = weakref.ref(func)

    class_.handler = add_handler_decorator
    return class_
