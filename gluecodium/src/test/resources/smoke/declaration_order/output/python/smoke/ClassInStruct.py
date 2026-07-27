

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.ClassInStructFooChecker import ClassInStructFooChecker


from _native_base import _NativeBase

import generated


class ClassInStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ClassInStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_ClassInStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

