

from __future__ import annotations

from smoke.SomeTypeCollectionError import SomeTypeCollectionError


from _native_base import _NativeBase

import generated


class SomeTypeCollection(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], SomeTypeCollection):
            super().__init__(args[0])
        else:
            super().__init__(generated.SomeTypeCollection(*args))

