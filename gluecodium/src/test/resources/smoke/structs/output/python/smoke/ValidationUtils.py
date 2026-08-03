

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class ValidationUtils(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ValidationUtils):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_ValidationUtils(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    class ValidationErrorCode(Enum):
    
        NONE = generated.smoke_ValidationUtilsValidationErrorCode.NONE
        VALIDATION_FAILED = generated.smoke_ValidationUtilsValidationErrorCode.VALIDATION_FAILED
    
        @property
        def _native(self):
            return self.value
    
    
    
    class ValidationError(Exception):
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    

