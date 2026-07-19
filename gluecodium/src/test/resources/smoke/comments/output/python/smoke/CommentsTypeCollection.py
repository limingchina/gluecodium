

from __future__ import annotations



from _native_base import _NativeBase

import generated


class CommentsTypeCollection(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.CommentsTypeCollection):
            super().__init__(args[0])
        else:
            super().__init__(generated.CommentsTypeCollection(*[getattr(arg, "_native", arg) for arg in args]))


    TYPE_COLLECTION_CONSTANT = True

