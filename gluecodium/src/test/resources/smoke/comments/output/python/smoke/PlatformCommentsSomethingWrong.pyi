

from smoke.PlatformCommentsSomeEnum import PlatformCommentsSomeEnum
import typing

class PlatformCommentsSomethingWrong(Exception):
    """An  when something goes wrong."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

