

from smoke.StructsWithMethodsVector import StructsWithMethodsVector
from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode


from _native_base import _NativeBase

import generated


class StructsWithMethods(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsWithMethods):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsWithMethods(*[getattr(arg, "_native", arg) for arg in args]))

