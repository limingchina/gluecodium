

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.ValidationUtils import ValidationUtils

class StructsWithMethodsInterface(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    class Vector3(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsWithMethodsInterfaceVector3):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_StructsWithMethodsInterfaceVector3(
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
    
    
        @property
        def z(self) -> float:
            return _wrap(self._native.z, float)
        @z.setter
        def z(self, value: float):
          self._native.z = _unwrap(value, float)
    
    
        def distance_to(self, other: StructsWithMethodsInterface.Vector3) -> float:
            return _wrap(self._native.distance_to(_unwrap(other, StructsWithMethodsInterface.Vector3)), float)
    
        def add(self, other: StructsWithMethodsInterface.Vector3) -> StructsWithMethodsInterface.Vector3:
            return _wrap(self._native.add(_unwrap(other, StructsWithMethodsInterface.Vector3)), StructsWithMethodsInterface.Vector3)
    
        @staticmethod
        def validate(x: float, y: float, z: float) -> bool:
            return generated.smoke_StructsWithMethodsInterfaceVector3.validate(_unwrap(x, float), _unwrap(y, float), _unwrap(z, float))
    
        @staticmethod
        def create(*args, **kwargs) -> StructsWithMethodsInterface.Vector3:
            native_result = generated.smoke_StructsWithMethodsInterfaceVector3.create(*[_unwrap(a) for a in args])
            return _get_or_create_wrapper(native_result, StructsWithMethodsInterface.Vector3)
    
    
    
    
    class StructWithStaticMethodsOnly(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsWithMethodsInterfaceStructWithStaticMethodsOnly):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_StructsWithMethodsInterfaceStructWithStaticMethodsOnly(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @staticmethod
        def do_stuff():
            generated.smoke_StructsWithMethodsInterfaceStructWithStaticMethodsOnly.do_stuff()
    
    

