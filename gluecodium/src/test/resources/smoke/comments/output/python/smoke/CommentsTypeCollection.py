

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class CommentsTypeCollection(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_CommentsTypeCollection):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_CommentsTypeCollection(*[_unwrap(arg) for arg in args]))


    TYPE_COLLECTION_CONSTANT = True

