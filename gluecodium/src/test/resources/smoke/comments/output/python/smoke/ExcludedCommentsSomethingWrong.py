

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.ExcludedCommentsSomeEnum import ExcludedCommentsSomeEnum

class ExcludedCommentsSomethingWrong(Exception):
    """This is some very useful exception."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

