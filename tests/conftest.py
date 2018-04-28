import typing

import pytest


from pycommand_bus import command


@pytest.fixture()
def exemplary_command() -> typing.Type:
    @command
    class Example:
        def __init__(self, data: str) -> None:
            self.data = data

        def __repr__(self) -> str:
            return '<{} data={}>'.format(self.__class__.__name__, self.data)

    return Example
