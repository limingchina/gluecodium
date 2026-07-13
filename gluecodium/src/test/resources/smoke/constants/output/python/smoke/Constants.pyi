

from smoke.BOOL_CONSTANT import BOOL_CONSTANT
from smoke.DOUBLE_CONSTANT import DOUBLE_CONSTANT
from smoke.ENUM_CONSTANT import ENUM_CONSTANT
from smoke.FLOAT_CONSTANT import FLOAT_CONSTANT
from smoke.INT_CONSTANT import INT_CONSTANT
from smoke.STRING_CONSTANT import STRING_CONSTANT
from smoke.UINT_CONSTANT import UINT_CONSTANT


from _native_base import _NativeBase

import generated


class Constants(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Constants):
            super().__init__(args[0])
        else:
            super().__init__(generated.Constants(*args))

