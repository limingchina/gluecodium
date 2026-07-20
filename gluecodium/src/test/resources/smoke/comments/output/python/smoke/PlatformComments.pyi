

from smoke.PlatformCommentsSomeEnum import PlatformCommentsSomeEnum
import typing

from _native_base import _NativeBase

import generated


class PlatformComments(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def do_nothing(self): ...

    def do_magic(self): ...

    def some_method_with_all_comments(self, input: str) -> bool: ...

    def some_deprecated_method(self): ...

