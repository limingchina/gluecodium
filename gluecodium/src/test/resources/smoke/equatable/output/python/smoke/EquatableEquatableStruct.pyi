

from smoke.EquatableNestedEquatableStruct import EquatableNestedEquatableStruct
from smoke.EquatableSomeEnum import EquatableSomeEnum
import typing


from _native_base import _NativeBase

import generated


class EquatableEquatableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_EquatableEquatableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_EquatableEquatableStruct(*[_unwrap(arg) for arg in args]))


    @property
    def bool_field(self) -> bool:
        """"""
        return _wrap(self._native.bool_field, bool)
    @bool_field.setter
    def bool_field(self, value: bool):
      self._native.bool_field = _unwrap(value, bool)



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
    def struct_field(self) -> EquatableNestedEquatableStruct:
        """"""
        return _wrap(self._native.struct_field, EquatableNestedEquatableStruct)
    @struct_field.setter
    def struct_field(self, value: EquatableNestedEquatableStruct):
      self._native.struct_field = _unwrap(value, EquatableNestedEquatableStruct)



    @property
    def enum_field(self) -> EquatableSomeEnum:
        """"""
        return _wrap(self._native.enum_field, EquatableSomeEnum)
    @enum_field.setter
    def enum_field(self, value: EquatableSomeEnum):
      self._native.enum_field = _unwrap(value, EquatableSomeEnum)



    @property
    def array_field(self) -> list[str]:
        """"""
        return _wrap(self._native.array_field, list[str])
    @array_field.setter
    def array_field(self, value: list[str]):
      self._native.array_field = _unwrap(value, list[str])



    @property
    def map_field(self) -> dict[int, str]:
        """"""
        return _wrap(self._native.map_field, dict[int, str])
    @map_field.setter
    def map_field(self, value: dict[int, str]):
      self._native.map_field = _unwrap(value, dict[int, str])


