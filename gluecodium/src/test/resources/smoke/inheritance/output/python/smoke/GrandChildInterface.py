

from smoke.ChildInterface import ChildInterface

class GrandChildInterface:
    """"""

    def __init__(self, native):
        self._native = native


    def grand_child_method(self):
        """"""
        return self._native.grand_child_method()

