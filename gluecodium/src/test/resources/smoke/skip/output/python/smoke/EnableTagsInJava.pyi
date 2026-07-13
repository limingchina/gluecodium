



from _native_base import _NativeBase

import generated


class EnableTagsInJava(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, EnableTagsInJava):
            super().__init__(native)
        else:
            super().__init__(generated.EnableTagsInJava())


    def enable_tagged(self):
        """"""
        return self._native.enable_tagged()


    def dont_enable_tagged(self):
        """"""
        return self._native.dont_enable_tagged()


    def enable_tagged_list(self):
        """"""
        return self._native.enable_tagged_list()

