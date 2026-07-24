

from smoke.DummyStruct import DummyStruct
import typing


from _native_base import _NativeBase

import generated


class SkipFieldInPlatformImmutable(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SkipFieldInPlatformImmutable):
            super().__init__(args[0])
        else:
            super().__init__(generated.SkipFieldInPlatformImmutable(*[_unwrap(arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)



    @property
    def string_field(self) -> DummyStruct:
        """"""
        return _wrap(self._native.string_field, DummyStruct)



    @property
    def bool_field(self) -> bool:
        """"""
        return _wrap(self._native.bool_field, bool)


