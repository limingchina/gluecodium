

from __future__ import annotations

from smoke.TYPE_COLLECTION_CONSTANT import TYPE_COLLECTION_CONSTANT


from _native_base import _NativeBase

import generated


class CommentsTypeCollection(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], CommentsTypeCollection):
            super().__init__(args[0])
        else:
            super().__init__(generated.CommentsTypeCollection(*args))

