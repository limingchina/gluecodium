

from __future__ import annotations

from smoke.StructsWithMethodsVector import StructsWithMethodsVector
from smoke.ValidationError import ValidationError
from smoke.ValidationErrorCode import ValidationErrorCode


from _native_base import _NativeBase

import generated


class StructsWithMethods(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructsWithMethods):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsWithMethods(*[getattr(arg, "_native", arg) for arg in args]))

