

from smoke.DeprecationCommentsSomeEnum import DeprecationCommentsSomeEnum
import typing

class DeprecationCommentsSomethingWrong(Exception):
    """"""
    message: str

    def __init__(self, message: str) -> None: ...

