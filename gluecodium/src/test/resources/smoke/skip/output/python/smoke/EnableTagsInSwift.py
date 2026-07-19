

from __future__ import annotations



import generated


class EnableTagsInSwift(generated.EnableTagsInSwift):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.EnableTagsInSwift):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def enable_tagged(self):
        """"""
        return generated.EnableTagsInSwift.enable_tagged(self)

    def dont_enable_tagged(self):
        """"""
        return generated.EnableTagsInSwift.dont_enable_tagged(self)

    def enable_tagged_list(self):
        """"""
        return generated.EnableTagsInSwift.enable_tagged_list(self)

