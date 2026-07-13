

from __future__ import annotations

from smoke.NestedStruct import NestedStruct
from smoke.SomeEnum import SomeEnum


from _native_base import _NativeBase

import generated


class OrderInStructWithFunctions(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], OrderInStructWithFunctions):
            super().__init__(args[0])
        else:
            super().__init__(generated.OrderInStructWithFunctions(*args))


    @property
    def some_field(self) -> str:
        """"""
        return self._native.some_field

    @some_field.setter
    def some_field(self, value: str):
        self._native.some_field = value



    def do_stuff(self, struct_foo: NestedStruct) -> SomeEnum:
        """"""
        return self._native.do_stuff(struct_foo._native)

from enum import Enum


class SomeEnum(Enum):
    """"""

    FOO = 0
    BAR = 1

