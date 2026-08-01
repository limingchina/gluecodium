

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class ExternalClass(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def some_method(self, some_parameter: int):
        return _wrap(self._native.some_method(_unwrap(some_parameter, int)), None)

    @property
    def some_property(self) -> str:
        return _wrap(self._native.some_property, str)


    class SomeStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ExternalClasssome_Struct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_ExternalClasssome_Struct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field(self) -> str:
            return _wrap(self._native.some_field, str)
        @some_field.setter
        def some_field(self, value: str):
          self._native.some_field = _unwrap(value, str)
    
    
    
    
    class SomeEnum(Enum):
    
        SOME_VALUE = 0
    
    

