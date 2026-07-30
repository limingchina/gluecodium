

import typing

class SwiftExternalCtor:

    field: str

    @staticmethod
    def make(field: str) -> SwiftExternalCtor:
        ...

