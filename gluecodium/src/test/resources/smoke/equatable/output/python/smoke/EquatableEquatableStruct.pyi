

from smoke.EquatableNestedEquatableStruct import EquatableNestedEquatableStruct
from smoke.EquatableSomeEnum import EquatableSomeEnum
import typing


from _native_base import _NativeBase

import generated


class EquatableEquatableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EquatableEquatableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.EquatableEquatableStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def bool_field(self) -> bool:
        """"""
        return self._native.bool_field
    @bool_field.setter
    def bool_field(self, value: bool):
      self._native.bool_field = getattr(value, "_native", value)



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
    def struct_field(self) -> EquatableNestedEquatableStruct:
        """"""
        return EquatableNestedEquatableStruct(self._native.struct_field)
    @struct_field.setter
    def struct_field(self, value: EquatableNestedEquatableStruct):
      self._native.struct_field = getattr(value, "_native", value)



    @property
    def enum_field(self) -> EquatableSomeEnum:
        """"""
        return EquatableSomeEnum(self._native.enum_field)
    @enum_field.setter
    def enum_field(self, value: EquatableSomeEnum):
      self._native.enum_field = getattr(value, "_native", value)



    @property
    def array_field(self) -> list[str]:
        """"""
        return self._native.array_field
    @array_field.setter
    def array_field(self, value: list[str]):
      self._native.array_field = getattr(value, "_native", value)



    @property
    def map_field(self) -> dict[int, str]:
        """"""
        return self._native.map_field
    @map_field.setter
    def map_field(self, value: dict[int, str]):
      self._native.map_field = getattr(value, "_native", value)


