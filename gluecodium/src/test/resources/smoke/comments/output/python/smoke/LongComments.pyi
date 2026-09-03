

from enum import Enum
import typing

class LongComments:
    """This is some very useful interface. There is a lot to say about this interface. at least it has a long comment.
This is a placeholder, which has multiple lines. Here we have continuation of the first line.
But this should be rendered in line below.
This too!"""

    def some_method_with_long_comment(self, input: str, ratio: float) -> float:
        """This is very important method. It has very important parameters. It has side effects."""
        ...


