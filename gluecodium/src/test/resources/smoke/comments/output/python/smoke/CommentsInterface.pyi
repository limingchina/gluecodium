

from smoke.bool import bool


from _native_base import _NativeBase

import generated


class CommentsInterface(_NativeBase):
    """This is some very useful interface."""

    def __init__(self, native=None):
        if isinstance(native, CommentsInterface):
            super().__init__(native)
        else:
            super().__init__(generated.CommentsInterface())

    This is some very useful method that measures the usefulness of its input.
    def some_method_with_all_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return self._native.some_method_with_all_comments(input)

    This is some very useful method that measures the usefulness of its input.
    def some_method_with_input_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return self._native.some_method_with_input_comments(input)

    This is some very useful method that measures the usefulness of its input.
    def some_method_with_output_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return self._native.some_method_with_output_comments(input)

    This is some very useful method that measures the usefulness of its input.
    def some_method_with_no_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return self._native.some_method_with_no_comments(input)

    This is some very useful method that does not measure the usefulness of its input.
    def some_method_without_return_type_with_all_comments(self, input: str):
        """This is some very useful method that does not measure the usefulness of its input."""
        return self._native.some_method_without_return_type_with_all_comments(input)

    This is some very useful method that does not measure the usefulness of its input.
    def some_method_without_return_type_with_no_comments(self, input: str):
        """This is some very useful method that does not measure the usefulness of its input."""
        return self._native.some_method_without_return_type_with_no_comments(input)

    This is some very useful method that measures the usefulness of something.
    def some_method_without_input_parameters_with_all_comments(self) -> bool:
        """This is some very useful method that measures the usefulness of something."""
        return self._native.some_method_without_input_parameters_with_all_comments()

    This is some very useful method that measures the usefulness of something.
    def some_method_without_input_parameters_with_no_comments(self) -> bool:
        """This is some very useful method that measures the usefulness of something."""
        return self._native.some_method_without_input_parameters_with_no_comments()


    def some_method_with_nothing(self):
        """"""
        return self._native.some_method_with_nothing()

    This is some very useful method that does nothing.
    def some_method_without_return_type_or_input_parameters(self):
        """This is some very useful method that does nothing."""
        return self._native.some_method_without_return_type_or_input_parameters()

    Some very useful property.
    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        return self._native.is_some_property

    @is_some_property.setter
    def is_some_property(self, value: bool):
        self._native.is_some_property = value

from enum import Enum


class SomeEnum(Enum):
    """This is some very useful enum."""

    USELESS = 0
    USEFUL = 1

This is some very useful constant.
VERY_USEFUL = True

