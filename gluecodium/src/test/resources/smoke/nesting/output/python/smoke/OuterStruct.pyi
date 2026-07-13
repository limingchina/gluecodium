

from smoke.Builder import Builder
from smoke.InnerEnum import InnerEnum
from smoke.InstantiationError import InstantiationError
from smoke.OuterStruct import OuterStruct

from _native_base import _NativeBase


class OuterStruct(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    field: str


    def do_nothing(self):
        """"""
        return self._native.do_nothing()

