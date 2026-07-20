

from smoke.off.NestedPackagesSomeStruct import NestedPackagesSomeStruct
import typing

from _native_base import _NativeBase

import generated


class NestedPackages(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def basic_method(input: NestedPackagesSomeStruct) -> NestedPackagesSomeStruct: ...

