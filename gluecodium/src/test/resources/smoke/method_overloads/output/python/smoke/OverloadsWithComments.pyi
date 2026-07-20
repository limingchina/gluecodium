

import typing

from _native_base import _NativeBase

import generated


class OverloadsWithComments(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @typing.overload
    def do_stuff(self): ...

    @typing.overload
    def do_stuff(self, stuff: str): ...

