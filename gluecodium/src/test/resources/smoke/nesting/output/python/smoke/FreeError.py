

from __future__ import annotations

from smoke.FreeEnum import FreeEnum

class FreeError(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

