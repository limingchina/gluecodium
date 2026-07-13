

from smoke.ParentClass import ParentClass

class ChildClassFromClass(
    ParentClass):
    """"""

    def __init__(self, native):
        self._native = native


    def child_class_method(self):
        """"""
        return self._native.child_class_method()

