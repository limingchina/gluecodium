

from smoke.SomeEnum import SomeEnum
from smoke.bool import bool


from _native_base import _NativeBase

import generated


class DeprecationComments(_NativeBase):
    """This is some very useful interface."""

    def __init__(self, native=None):
        if isinstance(native, DeprecationComments):
            super().__init__(native)
        else:
            super().__init__(generated.DeprecationComments())

    This is some very useful method that measures the usefulness of its input.
    def some_method_with_all_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return self._native.some_method_with_all_comments(input)

    Some very useful property.
    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        return self._native.is_some_property

    @is_some_property.setter
    def is_some_property(self, value: bool):
        self._native.is_some_property = value

    Describes the property but not accessors.
    @property
    def property_but_not_accessors(self) -> str:
        """Describes the property but not accessors."""
        return self._native.property_but_not_accessors

    @property_but_not_accessors.setter
    def property_but_not_accessors(self, value: str):
        self._native.property_but_not_accessors = value

from enum import Enum


class SomeEnum(Enum):
    """This is some very useful enum."""

    USELESS = 0

This is some very useful constant.
VERY_USEFUL = True

