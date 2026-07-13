


from _native_base import _NativeBase


class EnableTagsInDart(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def enable_tagged(self):
        """"""
        return self._native.enable_tagged()


    def dont_enable_tagged(self):
        """"""
        return self._native.dont_enable_tagged()


    def enable_tagged_list(self):
        """"""
        return self._native.enable_tagged_list()

