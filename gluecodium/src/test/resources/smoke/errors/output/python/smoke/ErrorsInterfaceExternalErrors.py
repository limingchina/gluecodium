

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class ErrorsInterfaceExternalErrors(Enum):
    """"""

    NONE = generated.ErrorsInterfaceExternalErrors.NONE
    BOOM = generated.ErrorsInterfaceExternalErrors.BOOM
    BUST = generated.ErrorsInterfaceExternalErrors.BUST

    @property
    def _native(self):
        return self.value

