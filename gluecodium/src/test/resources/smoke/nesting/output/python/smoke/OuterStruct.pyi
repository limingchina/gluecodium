

from smoke.Builder import Builder
from smoke.InnerEnum import InnerEnum
from smoke.InstantiationError import InstantiationError


from _native_base import _NativeBase

import generated


class OuterStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], OuterStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.OuterStruct(*args))


    @property
    def field(self) -> str:
        """"""
        return self._native.field

    @field.setter
    def field(self, value: str):
        self._native.field = value



    def do_nothing(self):
        """"""
        return self._native.do_nothing()

from enum import Enum


class InnerEnum(Enum):
    """"""

    FOO = 0
    BAR = 1

