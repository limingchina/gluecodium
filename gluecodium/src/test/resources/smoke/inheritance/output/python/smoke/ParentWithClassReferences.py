

from smoke.ChildClassFromClass import ChildClassFromClass
from smoke.ParentClass import ParentClass

class ParentWithClassReferences:
    """"""

    def __init__(self, native):
        self._native = native


    def class_function(self) -> ChildClassFromClass:
        """"""
        return self._native.class_function()


    @property
    def class_property(self) -> ParentClass:
        """"""
        return self._native.class_property


