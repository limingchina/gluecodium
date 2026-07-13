

from smoke.ChildClassFromClass import ChildClassFromClass
from smoke.ParentClass import ParentClass
from smoke.ParentWithClassReferences import ParentWithClassReferences

class ChildWithParentClassReferences(
    ParentWithClassReferences):
    """"""

    def __init__(self, native):
        self._native = native

