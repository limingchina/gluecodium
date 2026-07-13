

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
from smoke.ShouldNotInclude import ShouldNotInclude

from _native_base import _NativeBase


class ParentInterfaceWithIncludes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def root_method(self, input1: IncludableStruct, input2: IncludableEnum) -> IncludableClass:
        """"""
        return self._native.root_method(input1, input2)


    def not_in_java(self) -> ShouldNotInclude:
        """"""
        return self._native.not_in_java()


    @property
    def root_property(self) -> IncludableLambda:
        """"""
        return self._native.root_property



    @property
    def not_in_java_property(self) -> ShouldNotInclude:
        """"""
        return self._native.not_in_java_property


