

from smoke.EnumWithAlias import EnumWithAlias
from enum import Enum
import typing

class AliasError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...


