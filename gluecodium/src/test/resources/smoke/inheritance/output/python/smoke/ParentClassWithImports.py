

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct

class ParentClassWithImports:
    """"""

    def __init__(self, native):
        self._native = native


    def root_method(self, input1: IncludableStruct, input2: IncludableEnum) -> IncludableClass:
        """"""
        return self._native.root_method(input1, input2)


    @property
    def root_property(self) -> IncludableLambda:
        """"""
        return self._native.root_property


