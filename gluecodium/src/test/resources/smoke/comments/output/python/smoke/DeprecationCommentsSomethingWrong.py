

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.DeprecationCommentsSomeEnum import DeprecationCommentsSomeEnum

class DeprecationCommentsSomethingWrong(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

