

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
from smoke.ParentInterfaceWithIncludes import ParentInterfaceWithIncludes
from smoke.ShouldNotInclude import ShouldNotInclude


from _native_base import _NativeBase

import generated


class ChildClassWithIncludes(
    ParentInterfaceWithIncludes)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

