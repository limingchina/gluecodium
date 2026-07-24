

from smoke.ExcludedCommentsOnlySomeEnum import ExcludedCommentsOnlySomeEnum
import typing

class ExcludedCommentsOnlySomethingWrong(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

