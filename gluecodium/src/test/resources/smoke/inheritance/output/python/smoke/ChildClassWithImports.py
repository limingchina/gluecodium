

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
from smoke.ParentClassWithImports import ParentClassWithImports

class ChildClassWithImports(
    ParentClassWithImports):
    """"""

    def __init__(self, native):
        self._native = native

