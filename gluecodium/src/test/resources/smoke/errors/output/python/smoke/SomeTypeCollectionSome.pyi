

from smoke.SomeTypeCollectionSomeTypeCollectionError import SomeTypeCollectionSomeTypeCollectionError
import typing

class SomeTypeCollectionSome(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

