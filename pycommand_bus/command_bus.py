class CommandBus:

    def dispatch(self, command):
        attr_name = '_pycommand_bus_handler'
        try:
            handler_weak_ref = getattr(command, attr_name, None)
            handler = handler_weak_ref()
        except (AttributeError, TypeError):
            raise Exception('No handler for {!r}'.format(command))

        if handler:
            handler(command)
