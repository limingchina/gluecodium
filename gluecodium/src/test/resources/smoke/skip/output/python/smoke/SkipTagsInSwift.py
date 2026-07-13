

from __future__ import annotations



from _native_base import _NativeBase

import generated


class SkipTagsInSwift(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, SkipTagsInSwift):
            super().__init__(native)
        else:
            super().__init__(generated.SkipTagsInSwift())


    def skip_tagged(self):
        """"""
        return self._native.skip_tagged()


    def dont_skip_tagged(self):
        """"""
        return self._native.dont_skip_tagged()


    def skip_tagged_list(self):
        """"""
        return self._native.skip_tagged_list()

