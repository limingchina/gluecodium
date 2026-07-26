

import typing


from _native_base import _NativeBase

import generated


class StructConstantsSomeStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_StructConstantsSomeStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructConstantsSomeStruct(*[_unwrap(arg) for arg in args]))


    @property
    def string_field(self) -> str:
        """"""
        return _wrap(self._native.string_field, str)
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = _unwrap(value, str)



    @property
    def float_field(self) -> float:
        """"""
        return _wrap(self._native.float_field, float)
    @float_field.setter
    def float_field(self, value: float):
      self._native.float_field = _unwrap(value, float)


