

from smoke.ExcludedCommentsSomeEnum import ExcludedCommentsSomeEnum
import typing

class ExcludedCommentsSomethingWrong(Exception):
    """This is some very useful exception."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

