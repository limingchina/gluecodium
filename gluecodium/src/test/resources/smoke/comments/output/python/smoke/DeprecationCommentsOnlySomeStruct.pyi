

import typing


from _native_base import _NativeBase

import generated


class DeprecationCommentsOnlySomeStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_DeprecationCommentsOnlySomeStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DeprecationCommentsOnlySomeStruct(*[_unwrap(arg) for arg in args]))


    @property
    def some_field(self) -> bool:
        """"""
        return _wrap(self._native.some_field, bool)
    @some_field.setter
    def some_field(self, value: bool):
      self._native.some_field = _unwrap(value, bool)


