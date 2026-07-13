

from __future__ import annotations

from smoke.SkipProxy import SkipProxy
from smoke.SkippedEverywhere import SkippedEverywhere
from smoke.SkippedEverywhereEnum import SkippedEverywhereEnum


from _native_base import _NativeBase

import generated


class InheritFromSkipped(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, InheritFromSkipped):
            super().__init__(native)
        else:
            super().__init__(generated.InheritFromSkipped())

