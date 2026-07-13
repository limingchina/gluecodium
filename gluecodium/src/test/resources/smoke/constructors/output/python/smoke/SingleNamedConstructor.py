

from smoke.SingleNamedConstructor import SingleNamedConstructor

class SingleNamedConstructor:
    """"""

    def __init__(self, native):
        self._native = native


    def create(self) -> SingleNamedConstructor:
        """"""
        return self._native.create()

