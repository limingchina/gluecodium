

from smoke.EnumWithAlias import EnumWithAlias
import typing

class AliasError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

