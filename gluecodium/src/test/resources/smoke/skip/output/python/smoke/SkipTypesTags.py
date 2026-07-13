

from __future__ import annotations

from smoke.PLACE_HOLDER import PLACE_HOLDER


from _native_base import _NativeBase

import generated


class SkipTypesTags(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], SkipTypesTags):
            super().__init__(args[0])
        else:
            super().__init__(generated.SkipTypesTags(*args))

