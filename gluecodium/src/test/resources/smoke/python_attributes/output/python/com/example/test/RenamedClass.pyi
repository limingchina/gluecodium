

import typing

from _native_base import _NativeBase

import generated


class RenamedClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def visible_method(self, param: int) -> str: ...

