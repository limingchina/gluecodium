

import typing

class JavaExternalCtor:

    field: str

    @staticmethod
    def make(field: str) -> JavaExternalCtor:
        ...

