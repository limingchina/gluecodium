

from smoke.DeprecationCommentsSomeEnum import DeprecationCommentsSomeEnum
import typing

class DeprecationComments:
    """This is some very useful interface."""

    def some_method_with_all_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        ...

    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        ...

    @is_some_property.setter
    def is_some_property(self, value: bool) -> None:
        """Sets some very useful property."""
        ...

    @property
    def property_but_not_accessors(self) -> str:
        """Describes the property but not accessors."""
        ...

    @property_but_not_accessors.setter
    def property_but_not_accessors(self, value: str) -> None:
        ...

    #: This is some very useful constant.
    VERY_USEFUL = True

