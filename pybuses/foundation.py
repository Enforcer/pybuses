import inspect

from pybuses.types import (
    Subscribable,
    Listener,
)


def get_subscribed(listener: Listener) -> Subscribable:
    arg_spec = inspect.getfullargspec(listener)
    if inspect.ismethod(listener):
        allowed_args_len = 2
    else:
        allowed_args_len = 1
    if len(arg_spec.args) != allowed_args_len:
        raise ValueError('{} is not accepting a single argument!'.format(listener))
    annotated_arg = arg_spec.annotations.get(arg_spec.args[-1])
    return annotated_arg  # type: ignore
