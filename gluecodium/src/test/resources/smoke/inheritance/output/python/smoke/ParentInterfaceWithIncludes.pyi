

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
from smoke.ShouldNotInclude import ShouldNotInclude


from _native_base import _NativeBase

import generated


class ParentInterfaceWithIncludes(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ParentInterfaceWithIncludes):
            super().__init__(native)
        else:
            super().__init__(generated.ParentInterfaceWithIncludes())


    def root_method(self, input1: IncludableStruct, input2: IncludableEnum) -> IncludableClass:
        """"""
        return self._native.root_method(input1._native, input2._native)


    def not_in_java(self) -> ShouldNotInclude:
        """"""
        return self._native.not_in_java()


    @property
    def root_property(self) -> IncludableLambda:
        """"""
        return self._native.root_property

    @root_property.setter
    def root_property(self, value: IncludableLambda):
        self._native.root_property = value


    @property
    def not_in_java_property(self) -> ShouldNotInclude:
        """"""
        return self._native.not_in_java_property

    @not_in_java_property.setter
    def not_in_java_property(self, value: ShouldNotInclude):
        self._native.not_in_java_property = value

