

from smoke.ParentInterface import ParentInterface

class ChildInterface:
    """"""

    def __init__(self, native):
        self._native = native


    def child_method(self):
        """"""
        return self._native.child_method()

