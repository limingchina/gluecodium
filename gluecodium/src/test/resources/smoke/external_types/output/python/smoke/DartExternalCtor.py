

from smoke.DartExternalCtor import DartExternalCtor

class DartExternalCtor:
    """"""

    def __init__(self, native):
        self._native = native


    field: str


    def make(self, field: str) -> DartExternalCtor:
        """"""
        return self._native.make(field)

