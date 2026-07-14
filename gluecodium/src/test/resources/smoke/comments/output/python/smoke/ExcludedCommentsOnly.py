

from __future__ import annotations

from smoke.SomeEnum import SomeEnum
from smoke.SomethingWrongError import SomethingWrongError


from _native_base import _NativeBase

import generated


class ExcludedCommentsOnly(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """"""
        return self._native.some_method_with_all_comments(input_parameter)

    def some_method_without_return_type_or_input_parameters(self):
        """"""
        return self._native.some_method_without_return_type_or_input_parameters()


    @property
    def is_some_property(self) -> bool:
        """"""
        return self._native.is_some_property

    @is_some_property.setter
    def is_some_property(self, value: bool):
        self._native.is_some_property = value
from enum import Enum


class SomeEnum(Enum):
    """"""

    USELESS = 0



VERY_USEFUL = True

