

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.OuterInternalEnum import OuterInternalEnum

class OuterInternalError(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

