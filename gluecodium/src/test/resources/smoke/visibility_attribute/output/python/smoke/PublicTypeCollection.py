

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class PublicTypeCollection(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_PublicTypeCollection):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PublicTypeCollection(*[_unwrap(arg) for arg in args]))

