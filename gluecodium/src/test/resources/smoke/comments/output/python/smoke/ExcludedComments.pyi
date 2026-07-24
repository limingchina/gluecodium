

from smoke.ExcludedCommentsSomeEnum import ExcludedCommentsSomeEnum
from smoke.ExcludedCommentsSomethingWrong import ExcludedCommentsSomethingWrong
import typing

from _native_base import _NativeBase

import generated


class ExcludedComments(_NativeBase):
    """This is some very useful class."""

    def __init__(self, native):
        super().__init__(native)

    def some_method_with_all_comments(self, input_parameter: str) -> bool: ...

    def some_method_without_return_type_or_input_parameters(self): ...

    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        return _wrap(self._native.is_some_property, bool)

    @is_some_property.setter
    def is_some_property(self, value: bool):
        self._native.is_some_property = _unwrap(value, bool)

    This is some very useful constant.
    VERY_USEFUL = True

