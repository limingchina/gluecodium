

import typing


from _native_base import _NativeBase

import generated


class TypesWithDefaultsImmutableStructWithDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypesWithDefaultsImmutableStructWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypesWithDefaultsImmutableStructWithDefaults(*[_unwrap(arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)



    @property
    def uint_field(self) -> int:
        """"""
        return _wrap(self._native.uint_field, int)



    @property
    def float_field(self) -> float:
        """"""
        return _wrap(self._native.float_field, float)



    @property
    def double_field(self) -> float:
        """"""
        return _wrap(self._native.double_field, float)



    @property
    def bool_field(self) -> bool:
        """"""
        return _wrap(self._native.bool_field, bool)



    @property
    def string_field(self) -> str:
        """"""
        return _wrap(self._native.string_field, str)


