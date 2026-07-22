

from __future__ import annotations

from smoke.ErrorsInternal import ErrorsInternal
from smoke.ErrorsInternalErrorCode import ErrorsInternalErrorCode
from smoke.SomeTypeCollectionSome import SomeTypeCollectionSome
from smoke.SomeTypeCollectionSomeTypeCollectionError import SomeTypeCollectionSomeTypeCollectionError

from _native_base import _NativeBase

import generated


class FooBar(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def method_with_internal_error():
        """"""
        generated.FooBar.method_with_internal_error()

    @staticmethod
    def method_with_type_collection_error():
        """"""
        generated.FooBar.method_with_type_collection_error()

