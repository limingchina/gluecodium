

import typing


from _native_base import _NativeBase

import generated


class TypesWithDefaultsImmutableStructWithDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypesWithDefaultsImmutableStructWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypesWithDefaultsImmutableStructWithDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return self._native.int_field



    @property
    def uint_field(self) -> int:
        """"""
        return self._native.uint_field



    @property
    def float_field(self) -> float:
        """"""
        return self._native.float_field



    @property
    def double_field(self) -> float:
        """"""
        return self._native.double_field



    @property
    def bool_field(self) -> bool:
        """"""
        return self._native.bool_field



    @property
    def string_field(self) -> str:
        """"""
        return self._native.string_field


