

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.StructsAllTypesStruct import StructsAllTypesStruct


from _native_base import _NativeBase

import generated


class StructsNestingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsNestingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsNestingImmutableStruct(*[_unwrap(arg) for arg in args]))


    @property
    def struct_field(self) -> StructsAllTypesStruct:
        """"""
        return _wrap(self._native.struct_field, StructsAllTypesStruct)


