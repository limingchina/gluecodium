

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.PlatformNamesBasicStruct import PlatformNamesBasicStruct

from _native_base import _NativeBase

import generated


class PlatformNamesInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def basic_method(self, basic_parameter: str) -> PlatformNamesBasicStruct:
        """"""
        return _wrap(self._native.basic_method(_unwrap(basic_parameter, str)), PlatformNamesBasicStruct)

    @staticmethod
    def create(basic_parameter: str) -> PlatformNamesInterface:
        """"""
        native_result = generated.PlatformNamesInterface.create(_unwrap(basic_parameter, str))
        return PlatformNamesInterface(native_result)

    @property
    def basic_property(self) -> int:
        """"""
        return _wrap(self._native.basic_property, int)

    @basic_property.setter
    def basic_property(self, value: int):
        self._native.basic_property = _unwrap(value, int)

