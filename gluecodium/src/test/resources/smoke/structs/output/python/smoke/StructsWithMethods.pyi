

from smoke.StructsWithMethodsVector import StructsWithMethodsVector
from smoke.ValidationUtilsValidation import ValidationUtilsValidation
from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode
import typing


from _native_base import _NativeBase

import generated


class StructsWithMethods(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsWithMethods):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsWithMethods(*[_unwrap(arg) for arg in args]))

