

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class MethodOverloads(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def is_boolean(*args, **kwargs) -> bool:
        return _wrap(self._native.is_boolean(*[_unwrap(a) for a in args]), bool)








    def is_float(*args, **kwargs) -> bool:
        return _wrap(self._native.is_float(*[_unwrap(a) for a in args]), bool)


    class Point(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_MethodOverloadsPoint):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_MethodOverloadsPoint(
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
    
    
    
    
    list[str] = list[str]
    
    
    
    list[int] = list[int]
    
    

