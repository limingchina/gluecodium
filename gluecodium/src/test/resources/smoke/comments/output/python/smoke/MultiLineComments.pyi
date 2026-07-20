

import typing

from _native_base import _NativeBase

import generated


class MultiLineComments(_NativeBase):
    """This is some very useful interface.
There is a lot to say about this interface.
at least it has multiline comments.

I am a heading
--------------

And now comes a list:
* asterisk
* needs
* escaping

```Some example code;```"""

    def __init__(self, native):
        super().__init__(native)

    def some_method_with_long_comment(self, input: str, ratio: float) -> float: ...

