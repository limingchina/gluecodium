

from smoke.commentsSomeEnum import commentsSomeEnum
import typing

class commentsSomethingWrong(Exception):
    """This is some very useful exception."""
    message: str

    def __init__(self, message: str) -> None: ...

