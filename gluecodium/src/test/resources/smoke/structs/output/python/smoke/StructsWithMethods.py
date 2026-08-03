

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.ValidationUtils import ValidationUtils

class StructsWithMethods(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsWithMethods):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsWithMethods(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    class Vector(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsWithMethods.Vector):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_StructsWithMethods.Vector(
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
    
    
        def distance_to(self, other: StructsWithMethods.Vector) -> float:
            return _wrap(self._native.distance_to(_unwrap(other, StructsWithMethods.Vector)), float)
    
        def add(self, other: StructsWithMethods.Vector) -> StructsWithMethods.Vector:
            return _wrap(self._native.add(_unwrap(other, StructsWithMethods.Vector)), StructsWithMethods.Vector)
    
        @staticmethod
        def validate(x: float, y: float) -> bool:
            return generated.smoke_StructsWithMethods.Vector.validate(_unwrap(x, float), _unwrap(y, float))
    
        @staticmethod
        def create(*args, **kwargs) -> StructsWithMethods.Vector:
            native_result = generated.smoke_StructsWithMethods.Vector.create(*[_unwrap(a) for a in args])
            return _get_or_create_wrapper(native_result, StructsWithMethods.Vector)
    
    
    
    

