from pycommand_bus.command_decorator import CommandType


class Middleware:
    def before(self, command: CommandType) -> None:
        pass

    def after(self, command: CommandType) -> None:
        pass
