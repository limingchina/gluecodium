

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional
from typing import Callable

from smoke.LambdasDeclarationOrderSomeStruct import LambdasDeclarationOrderSomeStruct
from smoke.LambdasInterface import LambdasInterface
from smoke.LambdasWithStructuredTypesClassCallback import LambdasWithStructuredTypesClassCallback
from smoke.LambdasWithStructuredTypesStructCallback import LambdasWithStructuredTypesStructCallback

from _native_base import _NativeBase

import generated


class LambdasWithStructuredTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def do_class_stuff(self, callback: Callable[[LambdasInterface], None]):
        """"""
        return _wrap(self._native.do_class_stuff(_unwrap(callback, Callable[[LambdasInterface], None])), None)

    def do_struct_stuff(self, callback: Callable[[LambdasDeclarationOrderSomeStruct], None]):
        """"""
        return _wrap(self._native.do_struct_stuff(_unwrap(callback, Callable[[LambdasDeclarationOrderSomeStruct], None])), None)

