

from smoke.DeclarationOrderNestedStruct import DeclarationOrderNestedStruct
from smoke.DeclarationOrderSomeEnum import DeclarationOrderSomeEnum
import typing


from _native_base import _NativeBase

import generated


class DeclarationOrder(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeclarationOrder):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DeclarationOrder(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

