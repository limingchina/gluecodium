

from __future__ import annotations

from smoke.TypeCollectionPoint import TypeCollectionPoint


from _native_base import _NativeBase

import generated


class TypeCollectionAllTypesStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypeCollectionAllTypesStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypeCollectionAllTypesStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def int8_field(self) -> int:
        """"""
        return self._native.int8_field
    @int8_field.setter
    def int8_field(self, value: int):
      self._native.int8_field = getattr(value, "_native", value)



    @property
    def uint8_field(self) -> int:
        """"""
        return self._native.uint8_field
    @uint8_field.setter
    def uint8_field(self, value: int):
      self._native.uint8_field = getattr(value, "_native", value)



    @property
    def int16_field(self) -> int:
        """"""
        return self._native.int16_field
    @int16_field.setter
    def int16_field(self, value: int):
      self._native.int16_field = getattr(value, "_native", value)



    @property
    def uint16_field(self) -> int:
        """"""
        return self._native.uint16_field
    @uint16_field.setter
    def uint16_field(self, value: int):
      self._native.uint16_field = getattr(value, "_native", value)



    @property
    def int32_field(self) -> int:
        """"""
        return self._native.int32_field
    @int32_field.setter
    def int32_field(self, value: int):
      self._native.int32_field = getattr(value, "_native", value)



    @property
    def uint32_field(self) -> int:
        """"""
        return self._native.uint32_field
    @uint32_field.setter
    def uint32_field(self, value: int):
      self._native.uint32_field = getattr(value, "_native", value)



    @property
    def int64_field(self) -> int:
        """"""
        return self._native.int64_field
    @int64_field.setter
    def int64_field(self, value: int):
      self._native.int64_field = getattr(value, "_native", value)



    @property
    def uint64_field(self) -> int:
        """"""
        return self._native.uint64_field
    @uint64_field.setter
    def uint64_field(self, value: int):
      self._native.uint64_field = getattr(value, "_native", value)



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
    def boolean_field(self) -> bool:
        """"""
        return self._native.boolean_field
    @boolean_field.setter
    def boolean_field(self, value: bool):
      self._native.boolean_field = getattr(value, "_native", value)



    @property
    def bytes_field(self) -> bytes:
        """"""
        return self._native.bytes_field
    @bytes_field.setter
    def bytes_field(self, value: bytes):
      self._native.bytes_field = getattr(value, "_native", value)



    @property
    def point_field(self) -> TypeCollectionPoint:
        """"""
        return TypeCollectionPoint(self._native.point_field)
    @point_field.setter
    def point_field(self, value: TypeCollectionPoint):
      self._native.point_field = getattr(value, "_native", value)


