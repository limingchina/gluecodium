

from __future__ import annotations

from package.typesenum import typesenum


from _native_base import _NativeBase

import generated


class Types(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.Types):
            super().__init__(args[0])
        else:
            super().__init__(generated.Types(*[getattr(arg, "_native", arg) for arg in args]))


    CONST = enum.NaN

