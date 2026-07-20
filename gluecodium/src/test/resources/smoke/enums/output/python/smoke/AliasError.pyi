

from smoke.EnumWithAlias import EnumWithAlias
import typing

class AliasError(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

