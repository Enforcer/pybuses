from typing import (
    Any,
    Callable,
    Hashable,
    Type,
    Union,
)

Subscribable = Union[Type, Hashable]
Listener = Callable[[Any], None]
