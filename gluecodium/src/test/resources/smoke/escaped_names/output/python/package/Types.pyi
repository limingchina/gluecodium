

from package.typesenum import typesenum
from package.typesstruct import typesstruct
import typing


from _native_base import _NativeBase

import generated


class Types(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.package_Types):
            super().__init__(args[0])
        else:
            super().__init__(generated.package_Types(*[_unwrap(arg) for arg in args]))


    CONST = enum.NaN

