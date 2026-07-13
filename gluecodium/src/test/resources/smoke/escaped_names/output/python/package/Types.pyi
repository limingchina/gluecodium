

from package.Enum import Enum


from _native_base import _NativeBase

import generated


class Types(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Types):
            super().__init__(args[0])
        else:
            super().__init__(generated.Types(*args))

from enum import Enum


class Enum(Enum):
    """"""

    NA_N = 0


CONST = enum.NaN

