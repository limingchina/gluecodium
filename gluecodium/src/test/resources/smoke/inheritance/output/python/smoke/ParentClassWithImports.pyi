

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct

from _native_base import _NativeBase


class ParentClassWithImports(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def root_method(self, input1: IncludableStruct, input2: IncludableEnum) -> IncludableClass:
        """"""
        return self._native.root_method(input1, input2)


    @property
    def root_property(self) -> IncludableLambda:
        """"""
        return self._native.root_property


