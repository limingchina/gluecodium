

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

    def do_class_stuff(self, callback: LambdasWithStructuredTypesClassCallback):
        """"""
        return self._native.do_class_stuff(callback._native)

    def do_struct_stuff(self, callback: LambdasWithStructuredTypesStructCallback):
        """"""
        return self._native.do_struct_stuff(callback._native)

