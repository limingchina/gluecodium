

from smoke.StructsNestingImmutableStruct import StructsNestingImmutableStruct
import typing


from _native_base import _NativeBase

import generated


class StructsDoubleNestingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_StructsDoubleNestingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsDoubleNestingImmutableStruct(*[_unwrap(arg) for arg in args]))


    @property
    def nesting_struct_field(self) -> StructsNestingImmutableStruct:
        """"""
        return _wrap(self._native.nesting_struct_field, StructsNestingImmutableStruct)


