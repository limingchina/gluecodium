

from smoke.commentsSomeEnum import commentsSomeEnum
from smoke.commentsSomeStruct import commentsSomeStruct
from smoke.commentsSomethingWrong import commentsSomethingWrong
import typing

from _native_base import _NativeBase

import generated


class CommentsLinks(_NativeBase):
    """The nested types like [random_method] don't need full name prefix, but it's
possible to references other interfaces like [smoke.CommentsInterface] or other members
[comments.someMethodWithAllComments].

Weblinks are not modified like this [example1], [example2](http://www.example.com/2) or https://www.example.com/3.

[example1]: http://example.com/1"""

    def __init__(self, native):
        super().__init__(native)

    @typing.overload
    def random_method(self, input_parameter: commentsSomeEnum) -> commentsSomeEnum: ...

    @typing.overload
    def random_method(self, text: str, flag: bool): ...

