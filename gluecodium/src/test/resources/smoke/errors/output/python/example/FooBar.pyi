

from smoke.ErrorsInternal import ErrorsInternal
from smoke.ErrorsInternalErrorCode import ErrorsInternalErrorCode
from smoke.SomeTypeCollectionSome import SomeTypeCollectionSome
from smoke.SomeTypeCollectionSomeTypeCollectionError import SomeTypeCollectionSomeTypeCollectionError
import typing

class FooBar:

    @staticmethod
    def method_with_internal_error():
        ...

    @staticmethod
    def method_with_type_collection_error():
        ...

