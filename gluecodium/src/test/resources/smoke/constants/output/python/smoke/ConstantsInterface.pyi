

from smoke.ConstantsInterfaceStateEnum import ConstantsInterfaceStateEnum
import typing

from _native_base import _NativeBase

import generated


class ConstantsInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    BOOL_CONSTANT = True


    INT_CONSTANT = -11


    UINT_CONSTANT = 4294967295


    FLOAT_CONSTANT = 2.71


    DOUBLE_CONSTANT = -3.14


    STRING_CONSTANT = "Foo bar"


    ENUM_CONSTANT = ConstantsInterfaceStateEnum.ON

