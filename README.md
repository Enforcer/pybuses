Pythonic implementation of CQRS command bus 
====
Zero-dependencies, flexible implementation of Command Bus. *Python 3.6+ only* 
## Basic usage
```python
import contextlib
import typing

from pycommand_bus import (
    command,
    CommandBus,
    CommandType,
) 

# Firstly, create command class
@command
class MakeSandwich:
    def __init__(self, ingredients: typing.List[str]) -> None:
        self.ingredients = ingredients
        

# Then decorate callable responsible for handling command
@MakeSandwich.handler
def sandwich_maker(command: MakeSandwich):
    print(f'Making sandwich with {command.ingredients}!')
    
command_bus = CommandBus()
command_bus.handle(MakeSandwich(['cheese', 'ham']))
```

## Middlewares
Middlewares are lightweight plugins that let us inject custom logic before and after given command was handled.
```python
@contextlib.contextmanager
def example_middleware(command: CommandType) -> None:
    print(f'Before handling {command}')
    yield
    print(f'After handling {command}')
    
    
command_bus_with_middleware = CommandBus([example_middleware])
command_bus_with_middleware.handle(MakeSandwich(['cheese', 'ham']))
```
