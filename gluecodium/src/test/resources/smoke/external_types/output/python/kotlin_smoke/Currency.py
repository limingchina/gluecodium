

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class Currency(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.Currency):
            super().__init__(args[0])
        else:
            super().__init__(generated.Currency(*[_unwrap(arg) for arg in args]))


    @property
    def currency_code(self) -> str:
        """"""
        return _wrap(self._native.currency_code, str)



    @property
    def numeric_code(self) -> int:
        """"""
        return _wrap(self._native.numeric_code, int)


