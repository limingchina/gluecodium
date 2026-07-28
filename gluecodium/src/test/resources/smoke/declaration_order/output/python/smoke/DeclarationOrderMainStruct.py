

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.DeclarationOrderNestedStruct import DeclarationOrderNestedStruct
from smoke.DeclarationOrderSomeEnum import DeclarationOrderSomeEnum


from _native_base import _NativeBase

import generated


class DeclarationOrderMainStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeclarationOrderMainStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DeclarationOrderMainStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def struct_field(self) -> DeclarationOrderNestedStruct:
        """"""
        return _wrap(self._native.struct_field, DeclarationOrderNestedStruct)
    @struct_field.setter
    def struct_field(self, value: DeclarationOrderNestedStruct):
      self._native.struct_field = _unwrap(value, DeclarationOrderNestedStruct)



    @property
    def type_def_field(self) -> int:
        """"""
        return _wrap(self._native.type_def_field, int)
    @type_def_field.setter
    def type_def_field(self, value: int):
      self._native.type_def_field = _unwrap(value, int)



    @property
    def struct_array_field(self) -> list[DeclarationOrderNestedStruct]:
        """"""
        return _wrap(self._native.struct_array_field, list[DeclarationOrderNestedStruct])
    @struct_array_field.setter
    def struct_array_field(self, value: list[DeclarationOrderNestedStruct]):
      self._native.struct_array_field = _unwrap(value, list[DeclarationOrderNestedStruct])



    @property
    def map_field(self) -> dict[int, list[DeclarationOrderNestedStruct]]:
        """"""
        return _wrap(self._native.map_field, dict[int, list[DeclarationOrderNestedStruct]])
    @map_field.setter
    def map_field(self, value: dict[int, list[DeclarationOrderNestedStruct]]):
      self._native.map_field = _unwrap(value, dict[int, list[DeclarationOrderNestedStruct]])



    @property
    def enum_field(self) -> DeclarationOrderSomeEnum:
        """"""
        return _wrap(self._native.enum_field, DeclarationOrderSomeEnum)
    @enum_field.setter
    def enum_field(self, value: DeclarationOrderSomeEnum):
      self._native.enum_field = _unwrap(value, DeclarationOrderSomeEnum)


