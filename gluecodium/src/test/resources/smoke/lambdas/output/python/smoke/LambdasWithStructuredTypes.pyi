

from smoke.ClassCallback import ClassCallback
from smoke.LambdasDeclarationOrderSomeStruct import LambdasDeclarationOrderSomeStruct
from smoke.LambdasInterface import LambdasInterface
from smoke.StructCallback import StructCallback


from _native_base import _NativeBase

import generated


class LambdasWithStructuredTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def do_class_stuff(self, callback: ClassCallback):
        """"""
        return self._native.do_class_stuff(callback._native)

    def do_struct_stuff(self, callback: StructCallback):
        """"""
        return self._native.do_struct_stuff(callback._native)

