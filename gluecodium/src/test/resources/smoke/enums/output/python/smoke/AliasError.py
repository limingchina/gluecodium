

from __future__ import annotations

from smoke.EnumWithAlias import EnumWithAlias

class AliasError(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

