

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.StructsAllTypesStruct import StructsAllTypesStruct


from _native_base import _NativeBase

import generated


class StructsStructWithArrayOfImmutable(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsStructWithArrayOfImmutable):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsStructWithArrayOfImmutable(*[_unwrap(arg) for arg in args]))


    @property
    def array_field(self) -> list[StructsAllTypesStruct]:
        """"""
        return _wrap(self._native.array_field, list[StructsAllTypesStruct])


