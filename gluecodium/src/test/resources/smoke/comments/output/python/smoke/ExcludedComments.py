

from smoke.SomeEnum import SomeEnum
from smoke.SomethingWrongError import SomethingWrongError
from smoke.VERY_USEFUL import VERY_USEFUL
from smoke.bool import bool

from _native_base import _NativeBase


class ExcludedComments(_NativeBase):
    """This is some very useful class."""

    def __init__(self, native):
        super().__init__(native)

    This is some very useful method that measures the usefulness of its input.
    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return self._native.some_method_with_all_comments(input_parameter)

    This is some very useful method that does nothing.
    def some_method_without_return_type_or_input_parameters(self):
        """This is some very useful method that does nothing."""
        return self._native.some_method_without_return_type_or_input_parameters()

    Some very useful property.
    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        return self._native.is_some_property


