

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
from smoke.ParentInterfaceWithIncludes import ParentInterfaceWithIncludes
from smoke.ShouldNotInclude import ShouldNotInclude
import typing

class ChildClassWithIncludes(
    ParentInterfaceWithIncludes):

