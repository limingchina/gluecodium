

from __future__ import annotations

from smoke.InternalError import InternalError
from smoke.InternalErrorCode import InternalErrorCode
from smoke.SomeError import SomeError
from smoke.SomeTypeCollectionError import SomeTypeCollectionError


from _native_base import _NativeBase

import generated


class FooBar(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def method_with_internal_error():
        """"""
        native_result = generated.FooBar.method_with_internal_error()
        return None(native_result)

    @staticmethod

    def method_with_type_collection_error():
        """"""
        native_result = generated.FooBar.method_with_type_collection_error()
        return None(native_result)

