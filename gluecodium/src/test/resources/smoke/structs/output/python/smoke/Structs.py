

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.TypeCollection import TypeCollection

class Structs(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def swap_point_coordinates(input: Structs.Point) -> Structs.Point:
        native_result = generated.smoke_Structs.swap_point_coordinates(_unwrap(input, Structs.Point))
        return _get_or_create_wrapper(native_result, Structs.Point)

    @staticmethod
    def return_all_types_struct(input: Structs.AllTypesStruct) -> Structs.AllTypesStruct:
        native_result = generated.smoke_Structs.return_all_types_struct(_unwrap(input, Structs.AllTypesStruct))
        return _get_or_create_wrapper(native_result, Structs.AllTypesStruct)

    @staticmethod
    def create_point(x: float, y: float) -> TypeCollection.Point:
        native_result = generated.smoke_Structs.create_point(_unwrap(x, float), _unwrap(y, float))
        return _get_or_create_wrapper(native_result, TypeCollection.Point)

    @staticmethod
    def modify_all_types_struct(input: TypeCollection.AllTypesStruct) -> TypeCollection.AllTypesStruct:
        native_result = generated.smoke_Structs.modify_all_types_struct(_unwrap(input, TypeCollection.AllTypesStruct))
        return _get_or_create_wrapper(native_result, TypeCollection.AllTypesStruct)

    class Point(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_Structs.Point):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_Structs.Point(
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
    
    
        @staticmethod
        def from_polar(phi: float, r: float) -> Structs.Point:
            """This is some constructor, which constructs Point from polar coordinates."""
            native_result = generated.smoke_Structs.Point.from_polar(_unwrap(phi, float), _unwrap(r, float))
            return _get_or_create_wrapper(native_result, Structs.Point)
    
    
    
    class Line(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_Structs.Line):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_Structs.Line(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def a(self) -> Structs.Point:
            return _wrap(self._native.a, Structs.Point)
        @a.setter
        def a(self, value: Structs.Point):
          self._native.a = _unwrap(value, Structs.Point)
    
    
        @property
        def b(self) -> Structs.Point:
            return _wrap(self._native.b, Structs.Point)
        @b.setter
        def b(self, value: Structs.Point):
          self._native.b = _unwrap(value, Structs.Point)
    
    
    
    
    class AllTypesStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_Structs.AllTypesStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_Structs.AllTypesStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def int8_field(self) -> int:
            return _wrap(self._native.int8_field, int)
    
    
        @property
        def uint8_field(self) -> int:
            return _wrap(self._native.uint8_field, int)
    
    
        @property
        def int16_field(self) -> int:
            return _wrap(self._native.int16_field, int)
    
    
        @property
        def uint16_field(self) -> int:
            return _wrap(self._native.uint16_field, int)
    
    
        @property
        def int32_field(self) -> int:
            return _wrap(self._native.int32_field, int)
    
    
        @property
        def uint32_field(self) -> int:
            return _wrap(self._native.uint32_field, int)
    
    
        @property
        def int64_field(self) -> int:
            return _wrap(self._native.int64_field, int)
    
    
        @property
        def uint64_field(self) -> int:
            return _wrap(self._native.uint64_field, int)
    
    
        @property
        def float_field(self) -> float:
            return _wrap(self._native.float_field, float)
    
    
        @property
        def double_field(self) -> float:
            return _wrap(self._native.double_field, float)
    
    
        @property
        def string_field(self) -> str:
            return _wrap(self._native.string_field, str)
    
    
        @property
        def boolean_field(self) -> bool:
            return _wrap(self._native.boolean_field, bool)
    
    
        @property
        def bytes_field(self) -> bytes:
            return _wrap(self._native.bytes_field, bytes)
    
    
        @property
        def point_field(self) -> Structs.Point:
            return _wrap(self._native.point_field, Structs.Point)
    
    
    
    
    class NestingImmutableStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_Structs.NestingImmutableStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_Structs.NestingImmutableStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def struct_field(self) -> Structs.AllTypesStruct:
            return _wrap(self._native.struct_field, Structs.AllTypesStruct)
    
    
    
    
    class DoubleNestingImmutableStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_Structs.DoubleNestingImmutableStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_Structs.DoubleNestingImmutableStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def nesting_struct_field(self) -> Structs.NestingImmutableStruct:
            return _wrap(self._native.nesting_struct_field, Structs.NestingImmutableStruct)
    
    
    
    
    class StructWithArrayOfImmutable(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_Structs.StructWithArrayOfImmutable):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_Structs.StructWithArrayOfImmutable(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def array_field(self) -> list[Structs.AllTypesStruct]:
            return _wrap(self._native.array_field, list[Structs.AllTypesStruct])
    
    
    
    
    class ImmutableStructWithCppAccessors(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_Structs.ImmutableStructWithCppAccessors):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_Structs.ImmutableStructWithCppAccessors(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def trivial_int_field(self) -> int:
            return _wrap(self._native.trivial_int_field, int)
    
    
        @property
        def trivial_double_field(self) -> float:
            return _wrap(self._native.trivial_double_field, float)
    
    
        @property
        def nontrivial_string_field(self) -> str:
            return _wrap(self._native.nontrivial_string_field, str)
    
    
        @property
        def nontrivial_point_field(self) -> Structs.Point:
            return _wrap(self._native.nontrivial_point_field, Structs.Point)
    
    
        @property
        def nontrivial_optional_point(self):
            return _wrap(self._native.nontrivial_optional_point, Optional[Structs.Point])
    
    
    
    
    class MutableStructWithCppAccessors(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_Structs.MutableStructWithCppAccessors):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_Structs.MutableStructWithCppAccessors(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def trivial_int_field(self) -> int:
            return _wrap(self._native.trivial_int_field, int)
        @trivial_int_field.setter
        def trivial_int_field(self, value: int):
          self._native.trivial_int_field = _unwrap(value, int)
    
    
        @property
        def trivial_double_field(self) -> float:
            return _wrap(self._native.trivial_double_field, float)
        @trivial_double_field.setter
        def trivial_double_field(self, value: float):
          self._native.trivial_double_field = _unwrap(value, float)
    
    
        @property
        def nontrivial_string_field(self) -> str:
            return _wrap(self._native.nontrivial_string_field, str)
        @nontrivial_string_field.setter
        def nontrivial_string_field(self, value: str):
          self._native.nontrivial_string_field = _unwrap(value, str)
    
    
        @property
        def nontrivial_point_field(self) -> Structs.Point:
            return _wrap(self._native.nontrivial_point_field, Structs.Point)
        @nontrivial_point_field.setter
        def nontrivial_point_field(self, value: Structs.Point):
          self._native.nontrivial_point_field = _unwrap(value, Structs.Point)
    
    
        @property
        def nontrivial_optional_point(self):
            return _wrap(self._native.nontrivial_optional_point, Optional[Structs.Point])
        @nontrivial_optional_point.setter
        def nontrivial_optional_point(self, value):
          self._native.nontrivial_optional_point = _unwrap(value, Optional[Structs.Point])
    
    
    
    
    class FooBar(Enum):
    
        FOO = generated.smoke_Structs.FooBar.FOO
        BAR = generated.smoke_Structs.FooBar.BAR
    
        @property
        def _native(self):
            return self.value
    
    
    
    ArrayOfImmutable = list[AllTypesStruct]
    
    

