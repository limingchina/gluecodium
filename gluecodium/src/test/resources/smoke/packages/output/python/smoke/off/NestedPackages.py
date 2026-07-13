

from __future__ import annotations

from smoke.off.SomeStruct import SomeStruct


from _native_base import _NativeBase

import generated


class NestedPackages(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def basic_method(input: SomeStruct) -> SomeStruct:
        """"""
        native_result = generated.NestedPackages.basic_method(input)
        return SomeStruct(native_result)

