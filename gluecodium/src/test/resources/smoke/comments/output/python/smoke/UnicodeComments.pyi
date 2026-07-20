

from smoke.commentsSomeEnum import commentsSomeEnum
import typing

from _native_base import _NativeBase

import generated


class UnicodeComments(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def some_method_with_all_comments(self, input: str) -> bool: ...

