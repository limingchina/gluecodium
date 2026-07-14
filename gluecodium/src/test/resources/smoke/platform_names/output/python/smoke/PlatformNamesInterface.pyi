

from smoke.PlatformNamesBasicStruct import PlatformNamesBasicStruct


from _native_base import _NativeBase

import generated


class PlatformNamesInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def basic_method(self, basic_parameter: str) -> PlatformNamesBasicStruct:
        """"""
        return self._native.basic_method(basic_parameter)

    @staticmethod
    def create(basic_parameter: str) -> PlatformNamesInterface:
        """"""
        native_result = generated.PlatformNamesInterface.create(basic_parameter)
        return PlatformNamesInterface(native_result)


    @property
    def basic_property(self) -> int:
        """"""
        return self._native.basic_property

    @basic_property.setter
    def basic_property(self, value: int):
        self._native.basic_property = value

