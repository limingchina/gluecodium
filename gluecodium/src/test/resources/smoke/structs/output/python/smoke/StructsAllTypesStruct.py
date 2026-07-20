

from __future__ import annotations

from smoke.StructsPoint import StructsPoint


from _native_base import _NativeBase

import generated


class StructsAllTypesStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsAllTypesStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsAllTypesStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def int8_field(self) -> int:
        """"""
        return self._native.int8_field



    @property
    def uint8_field(self) -> int:
        """"""
        return self._native.uint8_field



    @property
    def int16_field(self) -> int:
        """"""
        return self._native.int16_field



    @property
    def uint16_field(self) -> int:
        """"""
        return self._native.uint16_field



    @property
    def int32_field(self) -> int:
        """"""
        return self._native.int32_field



    @property
    def uint32_field(self) -> int:
        """"""
        return self._native.uint32_field



    @property
    def int64_field(self) -> int:
        """"""
        return self._native.int64_field



    @property
    def uint64_field(self) -> int:
        """"""
        return self._native.uint64_field



    @property
    def float_field(self) -> float:
        """"""
        return self._native.float_field



    @property
    def double_field(self) -> float:
        """"""
        return self._native.double_field



    @property
    def string_field(self) -> str:
        """"""
        return self._native.string_field



    @property
    def boolean_field(self) -> bool:
        """"""
        return self._native.boolean_field



    @property
    def bytes_field(self) -> bytes:
        """"""
        return self._native.bytes_field



    @property
    def point_field(self) -> StructsPoint:
        """"""
        return StructsPoint(self._native.point_field)


