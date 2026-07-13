

from smoke.SingleNamelessConstructor import SingleNamelessConstructor

class SingleNamelessConstructor:
    """"""

    def __init__(self, native):
        self._native = native


    def create(self) -> SingleNamelessConstructor:
        """"""
        return self._native.create()

