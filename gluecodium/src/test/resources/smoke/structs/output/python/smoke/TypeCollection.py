

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
    
    
    
    
    class Line(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypeCollectionLine):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypeCollectionLine(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def a(self) -> TypeCollection.Point:
            return _wrap(self._native.a, TypeCollection.Point)
        @a.setter
        def a(self, value: TypeCollection.Point):
          self._native.a = _unwrap(value, TypeCollection.Point)
    
    
        @property
        def b(self) -> TypeCollection.Point:
            return _wrap(self._native.b, TypeCollection.Point)
        @b.setter
        def b(self, value: TypeCollection.Point):
          self._native.b = _unwrap(value, TypeCollection.Point)
    
    
    
    
    class AllTypesStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypeCollectionAllTypesStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypeCollectionAllTypesStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def int8_field(self) -> int:
            return _wrap(self._native.int8_field, int)
        @int8_field.setter
        def int8_field(self, value: int):
          self._native.int8_field = _unwrap(value, int)
    
    
        @property
        def uint8_field(self) -> int:
            return _wrap(self._native.uint8_field, int)
        @uint8_field.setter
        def uint8_field(self, value: int):
          self._native.uint8_field = _unwrap(value, int)
    
    
        @property
        def int16_field(self) -> int:
            return _wrap(self._native.int16_field, int)
        @int16_field.setter
        def int16_field(self, value: int):
          self._native.int16_field = _unwrap(value, int)
    
    
        @property
        def uint16_field(self) -> int:
            return _wrap(self._native.uint16_field, int)
        @uint16_field.setter
        def uint16_field(self, value: int):
          self._native.uint16_field = _unwrap(value, int)
    
    
        @property
        def int32_field(self) -> int:
            return _wrap(self._native.int32_field, int)
        @int32_field.setter
        def int32_field(self, value: int):
          self._native.int32_field = _unwrap(value, int)
    
    
        @property
        def uint32_field(self) -> int:
            return _wrap(self._native.uint32_field, int)
        @uint32_field.setter
        def uint32_field(self, value: int):
          self._native.uint32_field = _unwrap(value, int)
    
    
        @property
        def int64_field(self) -> int:
            return _wrap(self._native.int64_field, int)
        @int64_field.setter
        def int64_field(self, value: int):
          self._native.int64_field = _unwrap(value, int)
    
    
        @property
        def uint64_field(self) -> int:
            return _wrap(self._native.uint64_field, int)
        @uint64_field.setter
        def uint64_field(self, value: int):
          self._native.uint64_field = _unwrap(value, int)
    
    
        @property
        def float_field(self) -> float:
            return _wrap(self._native.float_field, float)
        @float_field.setter
        def float_field(self, value: float):
          self._native.float_field = _unwrap(value, float)
    
    
        @property
        def double_field(self) -> float:
            return _wrap(self._native.double_field, float)
        @double_field.setter
        def double_field(self, value: float):
          self._native.double_field = _unwrap(value, float)
    
    
        @property
        def string_field(self) -> str:
            return _wrap(self._native.string_field, str)
        @string_field.setter
        def string_field(self, value: str):
          self._native.string_field = _unwrap(value, str)
    
    
        @property
        def boolean_field(self) -> bool:
            return _wrap(self._native.boolean_field, bool)
        @boolean_field.setter
        def boolean_field(self, value: bool):
          self._native.boolean_field = _unwrap(value, bool)
    
    
        @property
        def bytes_field(self) -> bytes:
            return _wrap(self._native.bytes_field, bytes)
        @bytes_field.setter
        def bytes_field(self, value: bytes):
          self._native.bytes_field = _unwrap(value, bytes)
    
    
        @property
        def point_field(self) -> TypeCollection.Point:
            return _wrap(self._native.point_field, TypeCollection.Point)
        @point_field.setter
        def point_field(self, value: TypeCollection.Point):
          self._native.point_field = _unwrap(value, TypeCollection.Point)
    
    
    
    
    TypeCollection.Point = TypeCollection.Point
    
    

