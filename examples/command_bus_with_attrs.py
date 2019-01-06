import attr
from pybuses import CommandBus


@attr.s(frozen=True)
class Example:
    number: int = attr.ib()
    name: str = attr.ib()


def example_handler(command: Example) -> None:
    print(f'Inside handler of {type(command)} - got {command}!')


command_bus = CommandBus()
command_bus.subscribe(example_handler)
command_bus.handle(Example(number=1, name='Sebastian'))
