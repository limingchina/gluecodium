

from __future__ import annotations

from smoke.OuterInternalEnum import OuterInternalEnum

class OuterInternalError(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

