

from __future__ import annotations



from _native_base import _NativeBase

import generated


class CommentsTypeCollection(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], CommentsTypeCollection):
            super().__init__(args[0])
        else:
            super().__init__(generated.CommentsTypeCollection(*args))

from enum import Enum


class TypeCollectionEnum(Enum):
    """"""

    ITEM = 0


TYPE_COLLECTION_CONSTANT = True

