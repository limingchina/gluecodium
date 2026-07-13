

from smoke.ClassCallback import ClassCallback
from smoke.LambdasInterface import LambdasInterface
from smoke.SomeStruct import SomeStruct
from smoke.StructCallback import StructCallback

class LambdasWithStructuredTypes:
    """"""

    def __init__(self, native):
        self._native = native


    def do_class_stuff(self, callback: ClassCallback):
        """"""
        return self._native.do_class_stuff(callback)


    def do_struct_stuff(self, callback: StructCallback):
        """"""
        return self._native.do_struct_stuff(callback)

