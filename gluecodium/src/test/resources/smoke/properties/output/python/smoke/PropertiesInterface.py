

from __future__ import annotations

from smoke.PropertiesInterfaceExampleStruct import PropertiesInterfaceExampleStruct


from _native_base import _NativeBase

import generated


class PropertiesInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, PropertiesInterface):
            super().__init__(native)
        else:
            super().__init__(generated.PropertiesInterface())


    @property
    def struct_property(self) -> PropertiesInterfaceExampleStruct:
        """"""
        return self._native.struct_property

    @struct_property.setter
    def struct_property(self, value: PropertiesInterfaceExampleStruct):
        self._native.struct_property = value

