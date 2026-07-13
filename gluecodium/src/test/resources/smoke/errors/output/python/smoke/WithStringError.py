

from __future__ import annotations


class WithStringError(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

