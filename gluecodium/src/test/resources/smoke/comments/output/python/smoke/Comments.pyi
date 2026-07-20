

from smoke.commentsSomeEnum import commentsSomeEnum
import typing

from _native_base import _NativeBase

import generated


class Comments(_NativeBase):
    """This is some very useful ."""

    def __init__(self, native):
        super().__init__(native)

    def some_method_with_all_comments(self, input_parameter: str) -> bool: ...

    def some_method_with_input_comments(self, input: str) -> bool: ...

    def some_method_with_output_comments(self, input: str) -> bool: ...

    def some_method_with_no_comments(self, input: str) -> bool: ...

    def some_method_without_return_type_with_all_comments(self, input: str): ...

    def some_method_without_return_type_with_no_comments(self, input: str): ...

    def some_method_without_input_parameters_with_all_comments(self) -> bool: ...

    def some_method_without_input_parameters_with_no_comments(self) -> bool: ...

    def some_method_with_nothing(self): ...

    def some_method_without_return_type_or_input_parameters(self): ...

    def one_parameter_comment_only(self, undocumented: str, documented: str) -> str: ...

    def return_comment_only(self, undocumented: str) -> str: ...

    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        return self._native.is_some_property

    @is_some_property.setter
    def is_some_property(self, value: bool):
        self._native.is_some_property = value

    @property
    def only_getter_property(self) -> int:
        """OnlyGetterProperty, which does not have a setter."""
        return self._native.only_getter_property


    @property
    def is_is_visible(self) -> bool:
        """A flag that determines if [OnlyGetterProperty] is visible on the screen."""
        return self._native.is_is_visible

    @is_is_visible.setter
    def is_is_visible(self, value: bool):
        self._native.is_is_visible = value

    This is some very useful constant.
    VERY_USEFUL = True

