

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.StructsNestingImmutableStruct import StructsNestingImmutableStruct


from _native_base import _NativeBase

import generated


class StructsDoubleNestingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsDoubleNestingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsDoubleNestingImmutableStruct(*[_unwrap(arg) for arg in args]))


    @property
    def nesting_struct_field(self) -> StructsNestingImmutableStruct:
        """"""
        return _wrap(self._native.nesting_struct_field, StructsNestingImmutableStruct)


