

from smoke.DeprecationCommentsSomeEnum import DeprecationCommentsSomeEnum
import typing

class DeprecationCommentsSomethingWrong(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

