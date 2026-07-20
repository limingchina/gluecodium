

from __future__ import annotations

from smoke.SerializationNestedSerializableStruct import SerializationNestedSerializableStruct
from smoke.SerializationSomeEnum import SerializationSomeEnum


from _native_base import _NativeBase

import generated


class SerializationSerializableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SerializationSerializableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.SerializationSerializableStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def bool_field(self) -> bool:
        """"""
        return self._native.bool_field
    @bool_field.setter
    def bool_field(self, value: bool):
      self._native.bool_field = getattr(value, "_native", value)



    @property
    def byte_field(self) -> int:
        """"""
        return self._native.byte_field
    @byte_field.setter
    def byte_field(self, value: int):
      self._native.byte_field = getattr(value, "_native", value)



    @property
    def short_field(self) -> int:
        """"""
        return self._native.short_field
    @short_field.setter
    def short_field(self, value: int):
      self._native.short_field = getattr(value, "_native", value)



    @property
    def int_field(self) -> int:
        """"""
        return self._native.int_field
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = getattr(value, "_native", value)



    @property
    def long_field(self) -> int:
        """"""
        return self._native.long_field
    @long_field.setter
    def long_field(self, value: int):
      self._native.long_field = getattr(value, "_native", value)



    @property
    def float_field(self) -> float:
        """"""
        return self._native.float_field
    @float_field.setter
    def float_field(self, value: float):
      self._native.float_field = getattr(value, "_native", value)



    @property
    def double_field(self) -> float:
        """"""
        return self._native.double_field
    @double_field.setter
    def double_field(self, value: float):
      self._native.double_field = getattr(value, "_native", value)



    @property
    def string_field(self) -> str:
        """"""
        return self._native.string_field
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = getattr(value, "_native", value)



    @property
    def struct_field(self) -> SerializationNestedSerializableStruct:
        """"""
        return SerializationNestedSerializableStruct(self._native.struct_field)
    @struct_field.setter
    def struct_field(self, value: SerializationNestedSerializableStruct):
      self._native.struct_field = getattr(value, "_native", value)



    @property
    def byte_buffer_field(self) -> bytes:
        """"""
        return self._native.byte_buffer_field
    @byte_buffer_field.setter
    def byte_buffer_field(self, value: bytes):
      self._native.byte_buffer_field = getattr(value, "_native", value)



    @property
    def array_field(self) -> list[str]:
        """"""
        return self._native.array_field
    @array_field.setter
    def array_field(self, value: list[str]):
      self._native.array_field = getattr(value, "_native", value)



    @property
    def struct_array_field(self) -> list[SerializationNestedSerializableStruct]:
        """"""
        return self._native.struct_array_field
    @struct_array_field.setter
    def struct_array_field(self, value: list[SerializationNestedSerializableStruct]):
      self._native.struct_array_field = getattr(value, "_native", value)



    @property
    def map_field(self) -> dict[int, str]:
        """"""
        return self._native.map_field
    @map_field.setter
    def map_field(self, value: dict[int, str]):
      self._native.map_field = getattr(value, "_native", value)



    @property
    def set_field(self) -> set[str]:
        """"""
        return self._native.set_field
    @set_field.setter
    def set_field(self, value: set[str]):
      self._native.set_field = getattr(value, "_native", value)



    @property
    def enum_set_field(self) -> set[SerializationSomeEnum]:
        """"""
        return self._native.enum_set_field
    @enum_set_field.setter
    def enum_set_field(self, value: set[SerializationSomeEnum]):
      self._native.enum_set_field = getattr(value, "_native", value)



    @property
    def enum_field(self) -> SerializationSomeEnum:
        """"""
        return SerializationSomeEnum(self._native.enum_field)
    @enum_field.setter
    def enum_field(self, value: SerializationSomeEnum):
      self._native.enum_field = getattr(value, "_native", value)


