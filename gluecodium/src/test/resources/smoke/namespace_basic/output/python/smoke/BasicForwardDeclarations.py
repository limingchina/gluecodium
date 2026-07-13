

from smoke.Basic import Basic

class BasicForwardDeclarations:
    """"""

    def __init__(self, native):
        self._native = native


    def use_basic(self) -> Basic:
        """"""
        return self._native.use_basic()

