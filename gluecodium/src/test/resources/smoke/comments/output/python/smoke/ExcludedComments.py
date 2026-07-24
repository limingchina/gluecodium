

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.ExcludedCommentsSomeEnum import ExcludedCommentsSomeEnum
from smoke.ExcludedCommentsSomethingWrong import ExcludedCommentsSomethingWrong

from _native_base import _NativeBase

import generated


class ExcludedComments(_NativeBase):
    """This is some very useful class."""

    def __init__(self, native):
        super().__init__(native)

    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(self._native.some_method_with_all_comments(_unwrap(input_parameter, str)), bool)

    def some_method_without_return_type_or_input_parameters(self):
        """This is some very useful method that does nothing."""
        return _wrap(self._native.some_method_without_return_type_or_input_parameters(), None)

    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        return _wrap(self._native.is_some_property, bool)

    @is_some_property.setter
    def is_some_property(self, value: bool):
        self._native.is_some_property = _unwrap(value, bool)

    This is some very useful constant.
    VERY_USEFUL = True

