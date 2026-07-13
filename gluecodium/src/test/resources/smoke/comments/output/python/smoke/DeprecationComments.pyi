

from smoke.SomeEnum import SomeEnum
from smoke.VERY_USEFUL import VERY_USEFUL
from smoke.bool import bool

from _native_base import _NativeBase


class DeprecationComments(_NativeBase):
    """This is some very useful interface."""

    def __init__(self, native):
        super().__init__(native)

    This is some very useful method that measures the usefulness of its input.
    def some_method_with_all_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return self._native.some_method_with_all_comments(input)

    Some very useful property.
    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        return self._native.is_some_property


    Describes the property but not accessors.
    @property
    def property_but_not_accessors(self) -> str:
        """Describes the property but not accessors."""
        return self._native.property_but_not_accessors


