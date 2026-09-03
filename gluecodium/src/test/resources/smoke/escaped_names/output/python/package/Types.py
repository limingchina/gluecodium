

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class Types(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.package_Types):
            super().__init__(args[0])
        else:
            super().__init__(generated.package_Types(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    class Struct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.package_Types.Struct):
                super().__init__(args[0])
            else:
                super().__init__(generated.package_Types.Struct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def null(self) -> Types.Enum:
            return _wrap(self._native.null, Types.Enum)
        @null.setter
        def null(self, value: Types.Enum):
          self._native.null = _unwrap(value, Types.Enum)
    
    
    
    
    class Enum(Enum):
    
        NA_N = generated.package_Types.Enum.NA_N
    
        @property
        def _native(self):
            return self.value
    
    
    
    class ExceptionError(Exception):
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    
    
    ULong = list[Struct]
    
    

    CONST = Enum.NA_N

