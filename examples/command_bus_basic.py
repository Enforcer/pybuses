from typing import List

from pybuses import CommandBus


# Firstly, create command class
class MakeSandwich:
    def __init__(self, ingredients: List[str]) -> None:
        self.ingredients = ingredients


# Then create callable responsible for handling command.
# It must accept only one argument and is required to have type annotation for it.
def sandwich_maker(command: MakeSandwich) -> None:
    print(f'Making sandwich with {command.ingredients}!')


# finally, register the handler by subscribing
command_bus = CommandBus()
command_bus.subscribe(sandwich_maker)
command_bus.handle(MakeSandwich(['cheese', 'ham']))
