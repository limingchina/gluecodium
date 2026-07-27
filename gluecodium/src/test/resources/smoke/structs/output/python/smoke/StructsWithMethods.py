

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.StructsWithMethodsVector import StructsWithMethodsVector
from smoke.ValidationUtilsValidation import ValidationUtilsValidation
from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode


from _native_base import _NativeBase

import generated


class StructsWithMethods(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsWithMethods):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsWithMethods(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

