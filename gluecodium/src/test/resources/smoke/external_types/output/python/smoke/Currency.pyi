

from enum import Enum
import typing
from typing import Optional

class Currency:
    def __init__(self, currency_code: str, numeric_code: int) -> None: ...

    currency_code: str

    numeric_code: int
