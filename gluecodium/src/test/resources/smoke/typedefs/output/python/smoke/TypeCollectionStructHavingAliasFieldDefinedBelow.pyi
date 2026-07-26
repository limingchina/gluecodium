

import typing


from _native_base import _NativeBase

import generated


class TypeCollectionStructHavingAliasFieldDefinedBelow(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_TypeCollectionStructHavingAliasFieldDefinedBelow):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_TypeCollectionStructHavingAliasFieldDefinedBelow(*[_unwrap(arg) for arg in args]))


    @property
    def field(self) -> int:
        """"""
        return _wrap(self._native.field, int)
    @field.setter
    def field(self, value: int):
      self._native.field = _unwrap(value, int)


