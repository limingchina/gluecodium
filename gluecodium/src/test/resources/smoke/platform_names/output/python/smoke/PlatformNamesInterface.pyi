

from smoke.PlatformNamesBasicStruct import PlatformNamesBasicStruct
import typing

from _native_base import _NativeBase

import generated


class PlatformNamesInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def basic_method(self, basic_parameter: str) -> PlatformNamesBasicStruct: ...

    @staticmethod
    def create(basic_parameter: str) -> PlatformNamesInterface: ...

    @property
    def basic_property(self) -> int:
        """"""
        return _wrap(self._native.basic_property, int)

    @basic_property.setter
    def basic_property(self, value: int):
        self._native.basic_property = _unwrap(value, int)

