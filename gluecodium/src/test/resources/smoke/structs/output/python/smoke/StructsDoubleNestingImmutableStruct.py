

from __future__ import annotations

from smoke.StructsNestingImmutableStruct import StructsNestingImmutableStruct


from _native_base import _NativeBase

import generated


class StructsDoubleNestingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsDoubleNestingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsDoubleNestingImmutableStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def nesting_struct_field(self) -> StructsNestingImmutableStruct:
        """"""
        return StructsNestingImmutableStruct(self._native.nesting_struct_field)


