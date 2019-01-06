import inspect

from pybuses.types import (
    Subscribable,
    Listener,
)


def get_subscribed(listener: Listener) -> Subscribable:
    arg_spec = inspect.getfullargspec(listener)
    if len(arg_spec.args) != 1:
        raise ValueError('{} is not accepting a single argument!'.format(listener))
    annotated_arg = arg_spec.annotations.get(arg_spec.args[0])
    return annotated_arg  # type: ignore
