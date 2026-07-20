

from smoke.ErrorsInternalErrorCode import ErrorsInternalErrorCode
from smoke.SomeTypeCollectionSomeTypeCollectionError import SomeTypeCollectionSomeTypeCollectionError
import typing

from _native_base import _NativeBase

import generated


class FooBar(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def method_with_internal_error(): ...

    @staticmethod
    def method_with_type_collection_error(): ...

