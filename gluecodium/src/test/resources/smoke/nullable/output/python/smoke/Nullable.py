

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.SomeInterface import SomeInterface

class Nullable(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def method_with_string(self, input: Optional[str]) -> Optional[str]:
        return _wrap(self._native.method_with_string(_unwrap(input, Optional[str])), Optional[str])

    def method_with_boolean(self, input: Optional[bool]) -> Optional[bool]:
        return _wrap(self._native.method_with_boolean(_unwrap(input, Optional[bool])), Optional[bool])

    def method_with_double(self, input: Optional[float]) -> Optional[float]:
        return _wrap(self._native.method_with_double(_unwrap(input, Optional[float])), Optional[float])

    def method_with_int(self, input: Optional[int]) -> Optional[int]:
        return _wrap(self._native.method_with_int(_unwrap(input, Optional[int])), Optional[int])

    def method_with_some_struct(self, input: Optional[Nullable.SomeStruct]) -> Optional[Nullable.SomeStruct]:
        return _wrap(self._native.method_with_some_struct(_unwrap(input, Optional[Nullable.SomeStruct])), Optional[Nullable.SomeStruct])

    def method_with_some_enum(self, input: Optional[Nullable.SomeEnum]) -> Optional[Nullable.SomeEnum]:
        return _wrap(self._native.method_with_some_enum(_unwrap(input, Optional[Nullable.SomeEnum])), Optional[Nullable.SomeEnum])

    def method_with_some_array(self, input: Optional[list[str]]) -> Optional[list[str]]:
        return _wrap(self._native.method_with_some_array(_unwrap(input, Optional[list[str]])), Optional[list[str]])

    def method_with_inline_array(self, input: Optional[list[str]]) -> Optional[list[str]]:
        return _wrap(self._native.method_with_inline_array(_unwrap(input, Optional[list[str]])), Optional[list[str]])

    def method_with_some_map(self, input: Optional[dict[int, str]]) -> Optional[dict[int, str]]:
        return _wrap(self._native.method_with_some_map(_unwrap(input, Optional[dict[int, str]])), Optional[dict[int, str]])

    def method_with_instance(self, input: Optional[SomeInterface]) -> Optional[SomeInterface]:
        return _wrap(self._native.method_with_instance(_unwrap(input, Optional[SomeInterface])), Optional[SomeInterface])

    @property
    def string_property(self):
        return _wrap(self._native.string_property, Optional[str])

    @string_property.setter
    def string_property(self, value):
        self._native.string_property = _unwrap(value, Optional[str])

    @property
    def is_bool_property(self):
        return _wrap(self._native.is_bool_property, Optional[bool])

    @is_bool_property.setter
    def is_bool_property(self, value):
        self._native.is_bool_property = _unwrap(value, Optional[bool])

    @property
    def double_property(self):
        return _wrap(self._native.double_property, Optional[float])

    @double_property.setter
    def double_property(self, value):
        self._native.double_property = _unwrap(value, Optional[float])

    @property
    def int_property(self):
        return _wrap(self._native.int_property, Optional[int])

    @int_property.setter
    def int_property(self, value):
        self._native.int_property = _unwrap(value, Optional[int])

    @property
    def struct_property(self):
        return _wrap(self._native.struct_property, Optional[Nullable.SomeStruct])

    @struct_property.setter
    def struct_property(self, value):
        self._native.struct_property = _unwrap(value, Optional[Nullable.SomeStruct])

    @property
    def enum_property(self):
        return _wrap(self._native.enum_property, Optional[Nullable.SomeEnum])

    @enum_property.setter
    def enum_property(self, value):
        self._native.enum_property = _unwrap(value, Optional[Nullable.SomeEnum])

    @property
    def array_property(self):
        return _wrap(self._native.array_property, Optional[list[str]])

    @array_property.setter
    def array_property(self, value):
        self._native.array_property = _unwrap(value, Optional[list[str]])

    @property
    def inline_array_property(self):
        return _wrap(self._native.inline_array_property, Optional[list[str]])

    @inline_array_property.setter
    def inline_array_property(self, value):
        self._native.inline_array_property = _unwrap(value, Optional[list[str]])

    @property
    def map_property(self):
        return _wrap(self._native.map_property, Optional[dict[int, str]])

    @map_property.setter
    def map_property(self, value):
        self._native.map_property = _unwrap(value, Optional[dict[int, str]])

    @property
    def instance_property(self):
        return _wrap(self._native.instance_property, Optional[SomeInterface])

    @instance_property.setter
    def instance_property(self, value):
        self._native.instance_property = _unwrap(value, Optional[SomeInterface])

    class SomeStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_NullableSomeStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_NullableSomeStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def string_field(self) -> str:
            return _wrap(self._native.string_field, str)
        @string_field.setter
        def string_field(self, value: str):
          self._native.string_field = _unwrap(value, str)
    
    
    
    
    class NullableStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_NullableNullableStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_NullableNullableStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def string_field(self):
            return _wrap(self._native.string_field, Optional[str])
        @string_field.setter
        def string_field(self, value):
          self._native.string_field = _unwrap(value, Optional[str])
    
    
        @property
        def bool_field(self):
            return _wrap(self._native.bool_field, Optional[bool])
        @bool_field.setter
        def bool_field(self, value):
          self._native.bool_field = _unwrap(value, Optional[bool])
    
    
        @property
        def double_field(self):
            return _wrap(self._native.double_field, Optional[float])
        @double_field.setter
        def double_field(self, value):
          self._native.double_field = _unwrap(value, Optional[float])
    
    
        @property
        def struct_field(self):
            return _wrap(self._native.struct_field, Optional[Nullable.SomeStruct])
        @struct_field.setter
        def struct_field(self, value):
          self._native.struct_field = _unwrap(value, Optional[Nullable.SomeStruct])
    
    
        @property
        def enum_field(self):
            return _wrap(self._native.enum_field, Optional[Nullable.SomeEnum])
        @enum_field.setter
        def enum_field(self, value):
          self._native.enum_field = _unwrap(value, Optional[Nullable.SomeEnum])
    
    
        @property
        def array_field(self):
            return _wrap(self._native.array_field, Optional[list[str]])
        @array_field.setter
        def array_field(self, value):
          self._native.array_field = _unwrap(value, Optional[list[str]])
    
    
        @property
        def inline_array_field(self):
            return _wrap(self._native.inline_array_field, Optional[list[str]])
        @inline_array_field.setter
        def inline_array_field(self, value):
          self._native.inline_array_field = _unwrap(value, Optional[list[str]])
    
    
        @property
        def map_field(self):
            return _wrap(self._native.map_field, Optional[dict[int, str]])
        @map_field.setter
        def map_field(self, value):
          self._native.map_field = _unwrap(value, Optional[dict[int, str]])
    
    
        @property
        def instance_field(self):
            return _wrap(self._native.instance_field, Optional[SomeInterface])
        @instance_field.setter
        def instance_field(self, value):
          self._native.instance_field = _unwrap(value, Optional[SomeInterface])
    
    
    
    
    class NullableIntsStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_NullableNullableIntsStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_NullableNullableIntsStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def int8_field(self):
            return _wrap(self._native.int8_field, Optional[int])
        @int8_field.setter
        def int8_field(self, value):
          self._native.int8_field = _unwrap(value, Optional[int])
    
    
        @property
        def int16_field(self):
            return _wrap(self._native.int16_field, Optional[int])
        @int16_field.setter
        def int16_field(self, value):
          self._native.int16_field = _unwrap(value, Optional[int])
    
    
        @property
        def int32_field(self):
            return _wrap(self._native.int32_field, Optional[int])
        @int32_field.setter
        def int32_field(self, value):
          self._native.int32_field = _unwrap(value, Optional[int])
    
    
        @property
        def int64_field(self):
            return _wrap(self._native.int64_field, Optional[int])
        @int64_field.setter
        def int64_field(self, value):
          self._native.int64_field = _unwrap(value, Optional[int])
    
    
        @property
        def uint8_field(self):
            return _wrap(self._native.uint8_field, Optional[int])
        @uint8_field.setter
        def uint8_field(self, value):
          self._native.uint8_field = _unwrap(value, Optional[int])
    
    
        @property
        def uint16_field(self):
            return _wrap(self._native.uint16_field, Optional[int])
        @uint16_field.setter
        def uint16_field(self, value):
          self._native.uint16_field = _unwrap(value, Optional[int])
    
    
        @property
        def uint32_field(self):
            return _wrap(self._native.uint32_field, Optional[int])
        @uint32_field.setter
        def uint32_field(self, value):
          self._native.uint32_field = _unwrap(value, Optional[int])
    
    
        @property
        def uint64_field(self):
            return _wrap(self._native.uint64_field, Optional[int])
        @uint64_field.setter
        def uint64_field(self, value):
          self._native.uint64_field = _unwrap(value, Optional[int])
    
    
    
    
    class SomeEnum(Enum):
    
        ON = generated.smoke_NullableSomeEnum.ON
        OFF = generated.smoke_NullableSomeEnum.OFF
    
        @property
        def _native(self):
            return self.value
    
    
    
    SomeArray = list[str]
    
    
    
    SomeMap = dict[int, str]
    
    

