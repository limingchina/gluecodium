

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

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
        native_result = generated.smoke_OuterStructBuilder.create()
        return _get_or_create_wrapper(native_result, OuterStructBuilder)

    def field(self, value: str) -> OuterStructBuilder:
        """"""
        return _wrap(self._native.field(_unwrap(value, str)), OuterStructBuilder)

    def build(self) -> OuterStruct:
        """"""
        return _wrap(self._native.build(), OuterStruct)

