

from smoke.ParentInterface import ParentInterface

class ChildClassFromInterface(
    ParentInterface):
    """"""

    def __init__(self, native):
        self._native = native


    def child_class_method(self):
        """"""
        return self._native.child_class_method()

