

from smoke.StructsAllTypesStruct import StructsAllTypesStruct
import typing


from _native_base import _NativeBase

import generated


class StructsNestingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsNestingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsNestingImmutableStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def struct_field(self) -> StructsAllTypesStruct:
        """"""
        return _wrap(self._native.struct_field, StructsAllTypesStruct)


