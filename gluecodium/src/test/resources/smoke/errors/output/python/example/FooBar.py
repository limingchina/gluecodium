

from smoke.InternalError import InternalError
from smoke.InternalErrorCode import InternalErrorCode
from smoke.SomeError import SomeError
from smoke.SomeTypeCollectionError import SomeTypeCollectionError

class FooBar:
    """"""

    def __init__(self, native):
        self._native = native


    def method_with_internal_error(self):
        """"""
        return self._native.method_with_internal_error()


    def method_with_type_collection_error(self):
        """"""
        return self._native.method_with_type_collection_error()

