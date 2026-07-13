

from namerules.ExampleError import ExampleError
from namerules.ExampleErrorCode import ExampleErrorCode
from namerules.ExampleStruct import ExampleStruct


from _native_base import _NativeBase

import generated


class NameRules(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def create() -> NameRules:
        """"""
        native_result = generated.NameRules.create()
        return NameRules(native_result)


    def some_method(self, some_argument: ExampleStruct) -> float:
        """"""
        return self._native.some_method(some_argument._native)


    @property
    def int_property(self) -> int:
        """"""
        return self._native.int_property

    @int_property.setter
    def int_property(self, value: int):
        self._native.int_property = value


    @property
    def is_boolean_property(self) -> bool:
        """"""
        return self._native.is_boolean_property

    @is_boolean_property.setter
    def is_boolean_property(self, value: bool):
        self._native.is_boolean_property = value


    @property
    def struct_property(self) -> ExampleStruct:
        """"""
        return self._native.struct_property

    @struct_property.setter
    def struct_property(self, value: ExampleStruct):
        self._native.struct_property = value

