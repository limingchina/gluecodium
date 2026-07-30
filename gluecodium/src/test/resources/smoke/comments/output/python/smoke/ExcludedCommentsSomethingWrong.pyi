

from smoke.ExcludedCommentsSomeEnum import ExcludedCommentsSomeEnum
import typing

class ExcludedCommentsSomethingWrong(Exception):
    """This is some very useful exception."""
    message: str

    def __init__(self, message: str) -> None: ...

