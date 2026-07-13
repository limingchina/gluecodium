

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
from smoke.ParentClassWithImports import ParentClassWithImports


from _native_base import _NativeBase

import generated


class ChildClassWithImports(
    ParentClassWithImports)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

