

import typing

from _native_base import _NativeBase

import generated


class InternalClassWithComments(_NativeBase):
    """This looks internal"""

    def __init__(self, native):
        super().__init__(native)

    def do_nothing(self): ...

