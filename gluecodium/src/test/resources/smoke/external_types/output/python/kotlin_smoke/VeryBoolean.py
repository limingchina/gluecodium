

from kotlin_smoke.VeryBoolean import VeryBoolean

class VeryBoolean:
    """"""

    def __init__(self, native):
        self._native = native


    value: bool


    def make(self, value: bool) -> VeryBoolean:
        """"""
        return self._native.make(value)

