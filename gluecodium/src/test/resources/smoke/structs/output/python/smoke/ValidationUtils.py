

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode


from _native_base import _NativeBase

import generated


class ValidationUtils(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_ValidationUtils):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_ValidationUtils(*[_unwrap(arg) for arg in args]))

