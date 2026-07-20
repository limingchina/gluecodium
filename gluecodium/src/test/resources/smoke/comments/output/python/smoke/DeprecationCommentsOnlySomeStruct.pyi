

import typing


from _native_base import _NativeBase

import generated


class DeprecationCommentsOnlySomeStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DeprecationCommentsOnlySomeStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.DeprecationCommentsOnlySomeStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def some_field(self) -> bool:
        """"""
        return self._native.some_field
    @some_field.setter
    def some_field(self, value: bool):
      self._native.some_field = getattr(value, "_native", value)


