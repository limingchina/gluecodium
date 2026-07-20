

from __future__ import annotations

from smoke.off.NestedPackagesSomeStruct import NestedPackagesSomeStruct

from _native_base import _NativeBase

import generated


class NestedPackages(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def basic_method(input: NestedPackagesSomeStruct) -> NestedPackagesSomeStruct:
        """"""
        native_result = generated.NestedPackages.basic_method(input._native)
        return NestedPackagesSomeStruct(native_result)

