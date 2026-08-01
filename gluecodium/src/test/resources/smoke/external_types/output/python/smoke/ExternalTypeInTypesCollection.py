

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class ExternalTypeInTypesCollection(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ExternalTypeInTypesCollection):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_ExternalTypeInTypesCollection(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    class IntStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ExternalTypeInTypesCollectionIntStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_ExternalTypeInTypesCollectionIntStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def int_field(self) -> int:
            return _wrap(self._native.int_field, int)
        @int_field.setter
        def int_field(self, value: int):
          self._native.int_field = _unwrap(value, int)
    
    
    

