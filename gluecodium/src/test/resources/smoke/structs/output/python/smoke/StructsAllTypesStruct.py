

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.StructsPoint import StructsPoint


from _native_base import _NativeBase

import generated


class StructsAllTypesStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsAllTypesStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsAllTypesStruct(*[_unwrap(arg) for arg in args]))


    @property
    def int8_field(self) -> int:
        """"""
        return _wrap(self._native.int8_field, int)



    @property
    def uint8_field(self) -> int:
        """"""
        return _wrap(self._native.uint8_field, int)



    @property
    def int16_field(self) -> int:
        """"""
        return _wrap(self._native.int16_field, int)



    @property
    def uint16_field(self) -> int:
        """"""
        return _wrap(self._native.uint16_field, int)



    @property
    def int32_field(self) -> int:
        """"""
        return _wrap(self._native.int32_field, int)



    @property
    def uint32_field(self) -> int:
        """"""
        return _wrap(self._native.uint32_field, int)



    @property
    def int64_field(self) -> int:
        """"""
        return _wrap(self._native.int64_field, int)



    @property
    def uint64_field(self) -> int:
        """"""
        return _wrap(self._native.uint64_field, int)



    @property
    def float_field(self) -> float:
        """"""
        return _wrap(self._native.float_field, float)



    @property
    def double_field(self) -> float:
        """"""
        return _wrap(self._native.double_field, float)



    @property
    def string_field(self) -> str:
        """"""
        return _wrap(self._native.string_field, str)



    @property
    def boolean_field(self) -> bool:
        """"""
        return _wrap(self._native.boolean_field, bool)



    @property
    def bytes_field(self) -> bytes:
        """"""
        return _wrap(self._native.bytes_field, bytes)



    @property
    def point_field(self) -> StructsPoint:
        """"""
        return _wrap(self._native.point_field, StructsPoint)


