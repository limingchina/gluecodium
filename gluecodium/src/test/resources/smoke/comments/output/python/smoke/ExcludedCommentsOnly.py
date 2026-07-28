

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.ExcludedCommentsOnlySomeEnum import ExcludedCommentsOnlySomeEnum
from smoke.ExcludedCommentsOnlySomethingWrong import ExcludedCommentsOnlySomethingWrong

from _native_base import _NativeBase

import generated


class ExcludedCommentsOnly(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """"""
        return _wrap(self._native.some_method_with_all_comments(_unwrap(input_parameter, str)), bool)

    def some_method_without_return_type_or_input_parameters(self):
        """"""
        return _wrap(self._native.some_method_without_return_type_or_input_parameters(), None)

    @property
    def is_some_property(self) -> bool:
        """"""
        return _wrap(self._native.is_some_property, bool)

    @is_some_property.setter
    def is_some_property(self, value: bool):
        self._native.is_some_property = _unwrap(value, bool)


    VERY_USEFUL = True

