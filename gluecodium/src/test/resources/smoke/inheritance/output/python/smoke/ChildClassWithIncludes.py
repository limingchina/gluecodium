

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
from smoke.ParentInterfaceWithIncludes import ParentInterfaceWithIncludes
from smoke.ShouldNotInclude import ShouldNotInclude

class ChildClassWithIncludes(
    ParentInterfaceWithIncludes):
    """"""

    def __init__(self, native):
        self._native = native

