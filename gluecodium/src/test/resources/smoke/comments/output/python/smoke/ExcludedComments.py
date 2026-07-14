

from __future__ import annotations

from smoke.SomeEnum import SomeEnum
from smoke.SomethingWrongError import SomethingWrongError


from _native_base import _NativeBase

import generated


class ExcludedComments(_NativeBase):
    """This is some very useful class."""

    def __init__(self, native):
        super().__init__(native)

    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return self._native.some_method_with_all_comments(input_parameter)

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


This is some very useful constant.
VERY_USEFUL = True

