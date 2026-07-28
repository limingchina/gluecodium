

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.StructsNestingImmutableStruct import StructsNestingImmutableStruct


from _native_base import _NativeBase

import generated


class StructsDoubleNestingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsDoubleNestingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsDoubleNestingImmutableStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def nesting_struct_field(self) -> StructsNestingImmutableStruct:
        """"""
        return _wrap(self._native.nesting_struct_field, StructsNestingImmutableStruct)


