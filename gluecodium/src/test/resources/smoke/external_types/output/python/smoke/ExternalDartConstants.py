

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.Rectangle import Rectangle


from _native_base import _NativeBase

import generated


class ExternalDartConstants(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ExternalDartConstants):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_ExternalDartConstants(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    SMALL = {0, 0, 1, 1}

    BIG = {0, 0, 10, 10}

