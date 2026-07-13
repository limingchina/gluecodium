

from smoke.BOOL_CONSTANT import BOOL_CONSTANT
from smoke.DOUBLE_CONSTANT import DOUBLE_CONSTANT
from smoke.ENUM_CONSTANT import ENUM_CONSTANT
from smoke.FLOAT_CONSTANT import FLOAT_CONSTANT
from smoke.INT_CONSTANT import INT_CONSTANT
from smoke.STRING_CONSTANT import STRING_CONSTANT
from smoke.UINT_CONSTANT import UINT_CONSTANT

from _native_base import _NativeBase


class ConstantsInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

