

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class UnusedTopLevelEnum(Enum):

    DOESNT_WORK = generated.smoke_UnusedTopLevelEnum.DOESNT_WORK
    CRASHED_ANYWAY = generated.smoke_UnusedTopLevelEnum.CRASHED_ANYWAY

    @property
    def _native(self):
        return self.value


