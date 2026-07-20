

from __future__ import annotations



from _native_base import _NativeBase

import generated


class TypesWithDefaultsSomeImmutableStructWithDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypesWithDefaultsSomeImmutableStructWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypesWithDefaultsSomeImmutableStructWithDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return self._native.int_field


