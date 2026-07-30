

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.PlatformCommentsSomeEnum import PlatformCommentsSomeEnum
from smoke.PlatformCommentsSomethingWrong import PlatformCommentsSomethingWrong

from _native_base import _NativeBase

import generated


class PlatformComments(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def do_nothing(self):
        """This is some very useless method that ."""
        return _wrap(self._native.do_nothing(), None)

    def do_magic(self):
        return _wrap(self._native.do_magic(), None)

    def some_method_with_all_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input or \esc@pe{s}."""
        return _wrap(self._native.some_method_with_all_comments(_unwrap(input, str)), bool)

    def some_deprecated_method(self):
        """"""
        return _wrap(self._native.some_deprecated_method(), None)

