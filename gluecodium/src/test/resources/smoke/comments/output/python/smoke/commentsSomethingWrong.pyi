

from smoke.commentsSomeEnum import commentsSomeEnum
import typing

class commentsSomethingWrong(Exception):
    """This is some very useful exception."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

