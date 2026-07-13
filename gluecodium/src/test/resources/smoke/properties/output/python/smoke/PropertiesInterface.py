

from smoke.ExampleStruct import ExampleStruct

class PropertiesInterface:
    """"""

    def __init__(self, native):
        self._native = native


    @property
    def struct_property(self) -> ExampleStruct:
        """"""
        return self._native.struct_property


