import inspect
import typing

from pycommand_bus import types


class EventBus:

    def __init__(self) -> None:
        self._listeners: typing.Dict[types.EventType, typing.List[types.ListenerType]] = {}

    def register(self, listener: types.ListenerType) -> None:
        arg_spec = inspect.getfullargspec(listener)
        assert len(arg_spec.args) == 1
        annotated_arg = arg_spec.annotations.get(arg_spec.args[0])
        assert annotated_arg
        if annotated_arg not in self._listeners:
            self._listeners[annotated_arg] = []

        self._listeners[annotated_arg].append(listener)

    def post(self, event: types.EventType) -> None:
        event_class = type(event)
        if event_class not in self._listeners:
            return

        for listener in self._listeners[event_class]:
            listener(event)
