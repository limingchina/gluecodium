

from smoke.ExcludedCommentsSomeEnum import ExcludedCommentsSomeEnum
from smoke.ExcludedCommentsSomethingWrong import ExcludedCommentsSomethingWrong
import typing

class ExcludedComments:
    """This is some very useful class."""

    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
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

