

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class NameRulesExampleErrorCode(Enum):
    """"""

    NONE = generated.namerules_NameRulesExampleErrorCode.NONE
    FATAL = generated.namerules_NameRulesExampleErrorCode.FATAL

    @property
    def _native(self):
        return self.value

