

from __future__ import annotations

from smoke.OuterStruct import OuterStruct

from _native_base import _NativeBase

import generated


class OuterStructBuilder(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create() -> OuterStructBuilder:
        """"""
        native_result = generated.OuterStructBuilder.create()
        return OuterStructBuilder(native_result)

    def field(self, value: str) -> OuterStructBuilder:
        """"""
        return self._native.field(value)

    def build(self) -> OuterStruct:
        """"""
        return self._native.build()

