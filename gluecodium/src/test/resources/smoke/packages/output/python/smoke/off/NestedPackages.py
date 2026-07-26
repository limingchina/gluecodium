

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

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
        native_result = generated.smoke_off_NestedPackages.basic_method(_unwrap(input, NestedPackagesSomeStruct))
        return NestedPackagesSomeStruct(native_result)

