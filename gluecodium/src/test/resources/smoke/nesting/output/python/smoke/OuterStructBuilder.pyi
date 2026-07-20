

from smoke.OuterStruct import OuterStruct
import typing

from _native_base import _NativeBase

import generated


class OuterStructBuilder(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create() -> OuterStructBuilder: ...

    def field(self, value: str) -> OuterStructBuilder: ...

    def build(self) -> OuterStruct: ...

