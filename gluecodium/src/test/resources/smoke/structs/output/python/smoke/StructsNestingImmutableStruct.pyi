

from smoke.StructsAllTypesStruct import StructsAllTypesStruct
import typing


from _native_base import _NativeBase

import generated


class StructsNestingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsNestingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsNestingImmutableStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def struct_field(self) -> StructsAllTypesStruct:
        """"""
        return StructsAllTypesStruct(self._native.struct_field)


