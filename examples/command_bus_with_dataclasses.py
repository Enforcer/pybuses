from dataclasses import dataclass
from typing import List

from pybuses import CommandBus


@dataclass
class MakeSandwich:
    ingredients: List[str]


def handler(command: MakeSandwich) -> None:
    print(f'dataclass-based command: {command}')


command_bus = CommandBus()
command_bus.subscribe(handler)
command_bus.handle(MakeSandwich(['ham', 'butter']))
