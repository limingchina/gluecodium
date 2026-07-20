

import typing


from _native_base import _NativeBase

import generated


class TypeDefsStructHavingAliasFieldDefinedBelow(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypeDefsStructHavingAliasFieldDefinedBelow):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypeDefsStructHavingAliasFieldDefinedBelow(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def field(self) -> float:
        """"""
        return self._native.field
    @field.setter
    def field(self, value: float):
      self._native.field = getattr(value, "_native", value)


