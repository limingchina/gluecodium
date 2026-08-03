

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class TypeCollection(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypeCollection):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_TypeCollection(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    class Point(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypeCollectionPoint):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypeCollectionPoint(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def x(self) -> float:
            return _wrap(self._native.x, float)
        @x.setter
        def x(self, value: float):
          self._native.x = _unwrap(value, float)
    
    
        @property
        def y(self) -> float:
            return _wrap(self._native.y, float)
        @y.setter
        def y(self, value: float):
          self._native.y = _unwrap(value, float)
    
    
    
    
    class StructHavingAliasFieldDefinedBelow(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypeCollectionStructHavingAliasFieldDefinedBelow):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypeCollectionStructHavingAliasFieldDefinedBelow(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def field(self) -> int:
            return _wrap(self._native.field, int)
        @field.setter
        def field(self, value: int):
          self._native.field = _unwrap(value, int)
    
    
    
    
    PointTypeDef = Point
    
    
    
    StorageId = int
    
    

    INVALID_STORAGE_ID = 0

