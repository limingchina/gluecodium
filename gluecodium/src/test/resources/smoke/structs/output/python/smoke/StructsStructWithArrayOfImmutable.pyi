

from smoke.StructsAllTypesStruct import StructsAllTypesStruct
import typing


from _native_base import _NativeBase

import generated


class StructsStructWithArrayOfImmutable(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsStructWithArrayOfImmutable):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsStructWithArrayOfImmutable(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def array_field(self) -> list[StructsAllTypesStruct]:
        """"""
        return _wrap(self._native.array_field, list[StructsAllTypesStruct])


