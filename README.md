Pythonic implementations of Command and Event Buses 
====
[![Build Status](https://travis-ci.org/Enforcer/pybuses.svg?branch=master)](https://travis-ci.org/Enforcer/pybuses)
[![Coverage Status](https://coveralls.io/repos/github/Enforcer/pycommand_bus/badge.svg)](https://coveralls.io/github/Enforcer/pycommand_bus)

Zero-dependencies, flexible implementation of Command Bus. *Python 3.6+ only*
## Basic usage of CommandBus
```python
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
```

## Middlewares
Middlewares are lightweight plugins that let us inject custom logic before and after given command was handled.

Context managers are for now the only supported way of defining middlewares. They simplify exception handling and specifying whether middleware logic should be executed before or after handling event. 
```python
import contextlib
from typing import (
    Any,
    Generator,
)

@contextlib.contextmanager
def example_middleware(command: Any) -> Generator:
    print(f'Before handling {command}')
    yield
    print(f'After handling {command}')


command_bus = CommandBus([example_middleware])
command_bus.subscribe(sandwich_maker)
command_bus.handle(MakeSandwich(['cheese', 'ham']))
```


## Basic usage of EventBus
```python
from decimal import Decimal

from pybuses import EventBus


# Create event
class PaymentMade:
    amount: Decimal
    who: int

    def __init__(self, amount: Decimal, who: int) -> None:
        self.amount = amount
        self.who = who


def handler(payment_made: PaymentMade) -> None:
    print(f'Oh, cool! {payment_made.who} paid {payment_made.amount / 100}$!')


event_bus = EventBus()
event_bus.subscribe(handler)
event_bus.post(PaymentMade(Decimal('10.99'), 123))
```

## Similarities & differences between Event- and CommandBus
EventBus can have 0 or many handlers subscribed to every event, while CommandBus must have exactly one handler for each command.

CommandBus supports middlewares while EventBus does not.


## data classes compatible
Using [dataclasses](https://docs.python.org/3/library/dataclasses.html) for building commands/events is supported
```python
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
```

## attrs compatible
Using [attrs](http://attrs.org/) for building commands/events is supported
```python
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
```
