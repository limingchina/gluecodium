

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class UnusedTopLevelEnum(Enum):
    """"""

    DOESNT_WORK = generated.smoke_UnusedTopLevelEnum.DOESNT_WORK
    CRASHED_ANYWAY = generated.smoke_UnusedTopLevelEnum.CRASHED_ANYWAY

    @property
    def _native(self):
        return self.value

