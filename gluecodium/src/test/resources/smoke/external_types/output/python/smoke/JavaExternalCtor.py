

from smoke.JavaExternalCtor import JavaExternalCtor

class JavaExternalCtor:
    """"""

    def __init__(self, native):
        self._native = native


    field: str


    def make(self, field: str) -> JavaExternalCtor:
        """"""
        return self._native.make(field)

