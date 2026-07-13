

from smoke.ValidationErrorCode import ValidationErrorCode


from _native_base import _NativeBase

import generated


class ValidationUtils(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], ValidationUtils):
            super().__init__(args[0])
        else:
            super().__init__(generated.ValidationUtils(*args))

from enum import Enum


class ValidationErrorCode(Enum):
    """"""

    NONE = 0
    VALIDATION_FAILED = 1

