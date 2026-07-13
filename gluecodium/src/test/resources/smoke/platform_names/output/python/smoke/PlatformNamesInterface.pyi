

from smoke.BasicStruct import BasicStruct
from smoke.PlatformNamesInterface import PlatformNamesInterface

from _native_base import _NativeBase


class PlatformNamesInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def basic_method(self, basic_parameter: str) -> BasicStruct:
        """"""
        return self._native.basic_method(basic_parameter)


    def create(self, basic_parameter: str) -> PlatformNamesInterface:
        """"""
        return self._native.create(basic_parameter)


    @property
    def basic_property(self) -> int:
        """"""
        return self._native.basic_property


