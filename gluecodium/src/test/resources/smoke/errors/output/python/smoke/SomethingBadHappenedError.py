

from __future__ import annotations

from smoke.SomeInternalEnum import SomeInternalEnum

class SomethingBadHappenedError(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

