

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.SerializationNestedSerializableStruct import SerializationNestedSerializableStruct
from smoke.SerializationSomeEnum import SerializationSomeEnum


from _native_base import _NativeBase

import generated


class SerializationSerializableStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_SerializationSerializableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_SerializationSerializableStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def bool_field(self) -> bool:
        """"""
        return _wrap(self._native.bool_field, bool)
    @bool_field.setter
    def bool_field(self, value: bool):
      self._native.bool_field = _unwrap(value, bool)



    @property
    def byte_field(self) -> int:
        """"""
        return _wrap(self._native.byte_field, int)
    @byte_field.setter
    def byte_field(self, value: int):
      self._native.byte_field = _unwrap(value, int)



    @property
    def short_field(self) -> int:
        """"""
        return _wrap(self._native.short_field, int)
    @short_field.setter
    def short_field(self, value: int):
      self._native.short_field = _unwrap(value, int)



    @property
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = _unwrap(value, int)



    @property
    def long_field(self) -> int:
        """"""
        return _wrap(self._native.long_field, int)
    @long_field.setter
    def long_field(self, value: int):
      self._native.long_field = _unwrap(value, int)



    @property
    def float_field(self) -> float:
        """"""
        return _wrap(self._native.float_field, float)
    @float_field.setter
    def float_field(self, value: float):
      self._native.float_field = _unwrap(value, float)



    @property
    def double_field(self) -> float:
        """"""
        return _wrap(self._native.double_field, float)
    @double_field.setter
    def double_field(self, value: float):
      self._native.double_field = _unwrap(value, float)



    @property
    def string_field(self) -> str:
        """"""
        return _wrap(self._native.string_field, str)
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = _unwrap(value, str)



    @property
    def struct_field(self) -> SerializationNestedSerializableStruct:
        """"""
        return _wrap(self._native.struct_field, SerializationNestedSerializableStruct)
    @struct_field.setter
    def struct_field(self, value: SerializationNestedSerializableStruct):
      self._native.struct_field = _unwrap(value, SerializationNestedSerializableStruct)



    @property
    def byte_buffer_field(self) -> bytes:
        """"""
        return _wrap(self._native.byte_buffer_field, bytes)
    @byte_buffer_field.setter
    def byte_buffer_field(self, value: bytes):
      self._native.byte_buffer_field = _unwrap(value, bytes)



    @property
    def array_field(self) -> list[str]:
        """"""
        return _wrap(self._native.array_field, list[str])
    @array_field.setter
    def array_field(self, value: list[str]):
      self._native.array_field = _unwrap(value, list[str])



    @property
    def struct_array_field(self) -> list[SerializationNestedSerializableStruct]:
        """"""
        return _wrap(self._native.struct_array_field, list[SerializationNestedSerializableStruct])
    @struct_array_field.setter
    def struct_array_field(self, value: list[SerializationNestedSerializableStruct]):
      self._native.struct_array_field = _unwrap(value, list[SerializationNestedSerializableStruct])



    @property
    def map_field(self) -> dict[int, str]:
        """"""
        return _wrap(self._native.map_field, dict[int, str])
    @map_field.setter
    def map_field(self, value: dict[int, str]):
      self._native.map_field = _unwrap(value, dict[int, str])



    @property
    def set_field(self) -> set[str]:
        """"""
        return _wrap(self._native.set_field, set[str])
    @set_field.setter
    def set_field(self, value: set[str]):
      self._native.set_field = _unwrap(value, set[str])



    @property
    def enum_set_field(self) -> set[SerializationSomeEnum]:
        """"""
        return _wrap(self._native.enum_set_field, set[SerializationSomeEnum])
    @enum_set_field.setter
    def enum_set_field(self, value: set[SerializationSomeEnum]):
      self._native.enum_set_field = _unwrap(value, set[SerializationSomeEnum])



    @property
    def enum_field(self) -> SerializationSomeEnum:
        """"""
        return _wrap(self._native.enum_field, SerializationSomeEnum)
    @enum_field.setter
    def enum_field(self, value: SerializationSomeEnum):
      self._native.enum_field = _unwrap(value, SerializationSomeEnum)


