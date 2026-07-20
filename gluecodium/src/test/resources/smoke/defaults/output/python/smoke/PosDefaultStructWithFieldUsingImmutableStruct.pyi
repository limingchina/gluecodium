

from smoke.ImmutableStructWithDefaults import ImmutableStructWithDefaults
import typing


from _native_base import _NativeBase

import generated


class PosDefaultStructWithFieldUsingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.PosDefaultStructWithFieldUsingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.PosDefaultStructWithFieldUsingImmutableStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def some_field1(self) -> ImmutableStructWithDefaults:
        """"""
        return ImmutableStructWithDefaults(self._native.some_field1)


