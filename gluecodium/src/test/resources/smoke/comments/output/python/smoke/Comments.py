

from __future__ import annotations

from smoke.SomeEnum import SomeEnum
from smoke.SomethingWrongError import SomethingWrongError
from smoke.VERY_USEFUL import VERY_USEFUL
from smoke.bool import bool


from _native_base import _NativeBase

import generated


class Comments(_NativeBase):
    """This is some very useful ."""

    def __init__(self, native):
        super().__init__(native)

    This is some very useful method that measures the usefulness of its input.
    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return self._native.some_method_with_all_comments(input_parameter)

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


    def one_parameter_comment_only(self, undocumented: str, documented: str) -> str:
        """"""
        return self._native.one_parameter_comment_only(undocumented, documented)


    def return_comment_only(self, undocumented: str) -> str:
        """"""
        return self._native.return_comment_only(undocumented)

    Some very useful property.
    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        return self._native.is_some_property

    @is_some_property.setter
    def is_some_property(self, value: bool):
        self._native.is_some_property = value

    OnlyGetterProperty, which does not have a setter.
    @property
    def only_getter_property(self) -> int:
        """OnlyGetterProperty, which does not have a setter."""
        return self._native.only_getter_property


    A flag that determines if [OnlyGetterProperty] is visible on the screen.
    @property
    def is_is_visible(self) -> bool:
        """A flag that determines if [OnlyGetterProperty] is visible on the screen."""
        return self._native.is_is_visible

    @is_is_visible.setter
    def is_is_visible(self, value: bool):
        self._native.is_is_visible = value

