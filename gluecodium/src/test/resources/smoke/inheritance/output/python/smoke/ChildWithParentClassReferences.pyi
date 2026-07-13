

from smoke.ChildClassFromClass import ChildClassFromClass
from smoke.ParentClass import ParentClass
from smoke.ParentWithClassReferences import ParentWithClassReferences

from _native_base import _NativeBase


class ChildWithParentClassReferences(
    ParentWithClassReferences)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

