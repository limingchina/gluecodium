

from smoke.Errors import Errors
from smoke.SomeTypeCollection import SomeTypeCollection
from enum import Enum
import typing
from typing import Optional

class FooBar:

    @staticmethod
    def method_with_internal_error():
        ...

    @staticmethod
    def method_with_type_collection_error():
        ...
