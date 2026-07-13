

from smoke.SwiftConstructorOverloads import SwiftConstructorOverloads

class SwiftConstructorOverloads:
    """"""

    def __init__(self, native):
        self._native = native


    def make(self, input: str) -> SwiftConstructorOverloads:
        """"""
        return self._native.make(input)


    def make_do(self, throughput: str) -> SwiftConstructorOverloads:
        """"""
        return self._native.make_do(throughput)

