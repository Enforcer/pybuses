import typing

import pytest


@pytest.fixture()
def exemplary_command() -> typing.Type:
    class Example:
        def __init__(self, data: str) -> None:
            self.data = data

        def __repr__(self) -> str:
            return '<{} data={}>'.format(self.__class__.__name__, self.data)

    return Example
