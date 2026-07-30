

import typing

class CommentsInterface:
    """This is some very useful interface."""

    def some_method_with_all_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        ...

    def some_method_with_input_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        ...

    def some_method_with_output_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        ...

    def some_method_with_no_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        ...

    def some_method_without_return_type_with_all_comments(self, input: str):
        """This is some very useful method that does not measure the usefulness of its input."""
        ...

    def some_method_without_return_type_with_no_comments(self, input: str):
        """This is some very useful method that does not measure the usefulness of its input."""
        ...

    def some_method_without_input_parameters_with_all_comments(self) -> bool:
        """This is some very useful method that measures the usefulness of something."""
        ...

    def some_method_without_input_parameters_with_no_comments(self) -> bool:
        """This is some very useful method that measures the usefulness of something."""
        ...

    def some_method_with_nothing(self):
        ...

    def some_method_without_return_type_or_input_parameters(self):
        """This is some very useful method that does nothing."""
        ...

    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        ...

    @is_some_property.setter
    def is_some_property(self, value: bool) -> None:
        """Sets some very useful property."""
        ...

    #: This is some very useful constant.
    VERY_USEFUL = True

