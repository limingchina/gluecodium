

from smoke.SimpleClass import SimpleClass
from smoke.SimpleInterface import SimpleInterface
from smoke.forward.Class1 import Class1
from smoke.forward.Class2 import Class2

class UseForward:
    """"""

    def __init__(self, native):
        self._native = native


    def use_it(self, param1: Class1, param2: Class2, simple_class: SimpleClass, simple_interface: SimpleInterface):
        """"""
        return self._native.use_it(param1, param2, simple_class, simple_interface)

