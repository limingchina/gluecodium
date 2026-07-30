

from smoke.PlatformCommentsSomeEnum import PlatformCommentsSomeEnum
import typing

class PlatformCommentsSomethingWrong(Exception):
    """An  when something goes wrong."""
    message: str

    def __init__(self, message: str) -> None: ...

