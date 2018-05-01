Pythonic implementation of CQRS command bus 
====
[![Build Status](https://travis-ci.org/Enforcer/pycommand_bus.svg?branch=master)](https://travis-ci.org/Enforcer/pycommand_bus)
[![Coverage Status](https://coveralls.io/repos/github/Enforcer/pycommand_bus/badge.svg)](https://coveralls.io/github/Enforcer/pycommand_bus)

Zero-dependencies, flexible implementation of Command Bus. *Python 3.5+ only* 
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
def sandwich_maker(command: MakeSandwich) -> None:
    print(f'Making sandwich with {command.ingredients}!')
    
command_bus = CommandBus()
command_bus.handle(MakeSandwich(['cheese', 'ham']))
```

## Middlewares
Middlewares are lightweight plugins that let us inject custom logic before and after given command was handled.

Context managers are for now the only supported way of defining middlewares. They simplify exception handling and specifying whether middleware logic should be executed before or after handling event. 
```python
@contextlib.contextmanager
def example_middleware(command: CommandType) -> None:
    print(f'Before handling {command}')
    yield
    print(f'After handling {command}')
    
    
command_bus_with_middleware = CommandBus([example_middleware])
command_bus_with_middleware.handle(MakeSandwich(['cheese', 'ham']))
```

## attrs-compatible
Using [attrs](http://attrs.org/) for building commands is supported (and highly recommended).
```python
import attr
from pycommand_bus import (
    command,
    CommandBus,
)


@command
@attr.s(frozen=True)
class Example:
    number: int = attr.ib()
    name: str = attr.ib()


@Example.handler
def handleeee(command) -> None:
    print('handler!', command)


cb = CommandBus()
cb.handle(Example(number=1, name='Sebastian'))
```
