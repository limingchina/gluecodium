

from smoke.StructsAnotherExternalStruct import StructsAnotherExternalStruct
import typing


from _native_base import _NativeBase

import generated


class StructsExternalStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsExternalStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsExternalStruct(*[_unwrap(arg) for arg in args]))


    @property
    def string_field(self) -> str:
        """"""
        return _wrap(self._native.string_field, str)
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = _unwrap(value, str)



    @property
    def external_string_field(self) -> str:
        """"""
        return _wrap(self._native.external_string_field, str)
    @external_string_field.setter
    def external_string_field(self, value: str):
      self._native.external_string_field = _unwrap(value, str)



    @property
    def external_array_field(self) -> list[int]:
        """"""
        return _wrap(self._native.external_array_field, list[int])
    @external_array_field.setter
    def external_array_field(self, value: list[int]):
      self._native.external_array_field = _unwrap(value, list[int])



    @property
    def external_struct_field(self) -> StructsAnotherExternalStruct:
        """"""
        return _wrap(self._native.external_struct_field, StructsAnotherExternalStruct)
    @external_struct_field.setter
    def external_struct_field(self, value: StructsAnotherExternalStruct):
      self._native.external_struct_field = _unwrap(value, StructsAnotherExternalStruct)


