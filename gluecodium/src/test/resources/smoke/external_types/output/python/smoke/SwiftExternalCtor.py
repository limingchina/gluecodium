

from smoke.SwiftExternalCtor import SwiftExternalCtor

class SwiftExternalCtor:
    """"""

    def __init__(self, native):
        self._native = native


    field: str


    def make(self, field: str) -> SwiftExternalCtor:
        """"""
        return self._native.make(field)

