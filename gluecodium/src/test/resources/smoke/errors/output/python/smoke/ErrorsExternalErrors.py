

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class ErrorsExternalErrors(Enum):
    """"""

    NONE = generated.smoke_ErrorsExternalErrors.NONE
    BOOM = generated.smoke_ErrorsExternalErrors.BOOM
    BUST = generated.smoke_ErrorsExternalErrors.BUST

    @property
    def _native(self):
        return self.value

