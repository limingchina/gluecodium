

import typing

class SwiftConstructorOverloads:

    @staticmethod
    def make(input: str) -> SwiftConstructorOverloads:
        ...

    @staticmethod
    def make_do(throughput: str) -> SwiftConstructorOverloads:
        ...

