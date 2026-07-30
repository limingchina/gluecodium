

from smoke.ExcludedCommentsOnlySomeEnum import ExcludedCommentsOnlySomeEnum
import typing

class ExcludedCommentsOnlySomethingWrong(Exception):
    """"""
    message: str

    def __init__(self, message: str) -> None: ...

