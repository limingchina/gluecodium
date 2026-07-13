

from namerules.ExampleError import ExampleError
from namerules.ExampleErrorCode import ExampleErrorCode
from namerules.ExampleStruct import ExampleStruct
from namerules.NameRules import NameRules

class NameRules:
    """"""

    def __init__(self, native):
        self._native = native


    def create(self) -> NameRules:
        """"""
        return self._native.create()


    def some_method(self, some_argument: ExampleStruct) -> float:
        """"""
        return self._native.some_method(some_argument)


    @property
    def int_property(self) -> int:
        """"""
        return self._native.int_property



    @property
    def is_boolean_property(self) -> bool:
        """"""
        return self._native.is_boolean_property



    @property
    def struct_property(self) -> ExampleStruct:
        """"""
        return self._native.struct_property


