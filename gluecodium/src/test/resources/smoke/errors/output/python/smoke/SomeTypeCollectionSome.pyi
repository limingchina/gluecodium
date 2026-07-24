

from smoke.SomeTypeCollectionSomeTypeCollectionError import SomeTypeCollectionSomeTypeCollectionError
import typing

class SomeTypeCollectionSome(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

