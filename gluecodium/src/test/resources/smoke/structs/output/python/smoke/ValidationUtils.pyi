

from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode
import typing


from _native_base import _NativeBase

import generated


class ValidationUtils(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ValidationUtils):
            super().__init__(args[0])
        else:
            super().__init__(generated.ValidationUtils(*[_unwrap(arg) for arg in args]))

