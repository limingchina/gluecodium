

import typing


from _native_base import _NativeBase

import generated


class StructsAnotherExternalStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsAnotherExternalStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsAnotherExternalStruct(*[_unwrap(arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = _unwrap(value, int)


