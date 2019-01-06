import contextlib
from typing import (
    Any,
    Generator,
    List,
)

from pybuses import CommandBus


class MakeSandwich:
    def __init__(self, ingredients: List[str]) -> None:
        self.ingredients = ingredients


def sandwich_maker(command: MakeSandwich) -> None:
    print(f'Making sandwich with {command.ingredients}!')


@contextlib.contextmanager
def example_middleware(command: Any) -> Generator:
    print(f'Before handling {command}')
    yield
    print(f'After handling {command}')


command_bus = CommandBus([example_middleware])
command_bus.subscribe(sandwich_maker)
command_bus.handle(MakeSandwich(['cheese', 'ham']))
