

from smoke.FIRST_CONSTANT import FIRST_CONSTANT
from smoke.SomethingEnum import SomethingEnum

from _native_base import _NativeBase


class StructWithPosEnums(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    first_field: SomethingEnum


    explicit_field: SomethingEnum


    last_field: SomethingEnum

