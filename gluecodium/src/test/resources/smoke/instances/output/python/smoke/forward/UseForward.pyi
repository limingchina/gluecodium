

from smoke.SimpleClass import SimpleClass
from smoke.SimpleInterface import SimpleInterface
from smoke.forward.Class1 import Class1
from smoke.forward.Class2 import Class2


import generated


class UseForward(generated.UseForward):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.UseForward):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def use_it(self, param1: Class1, param2: Class2, simple_class: SimpleClass, simple_interface: SimpleInterface):
        """"""
        return generated.UseForward.use_it(self, param1._native, param2._native, simple_class._native, simple_interface._native)

