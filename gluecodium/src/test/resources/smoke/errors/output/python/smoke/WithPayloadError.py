

from __future__ import annotations

from smoke.Payload import Payload

class WithPayloadError(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

