

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct


from _native_base import _NativeBase

import generated


class ParentClassWithImports(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def root_method(self, input1: IncludableStruct, input2: IncludableEnum) -> IncludableClass:
        """"""
        return self._native.root_method(input1._native, input2._native)


    @property
    def root_property(self) -> IncludableLambda:
        """"""
        return self._native.root_property

    @root_property.setter
    def root_property(self, value: IncludableLambda):
        self._native.root_property = value

