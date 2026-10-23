

from smoke.EnumWithAlias import EnumWithAlias
from enum import Enum
import typing
from typing import Optional

class AliasError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...
