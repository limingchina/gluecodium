


from _native_base import _NativeBase


class SkipTagsInDart(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def skip_tagged(self):
        """"""
        return self._native.skip_tagged()


    def dont_skip_tagged(self):
        """"""
        return self._native.dont_skip_tagged()


    def skip_tagged_list(self):
        """"""
        return self._native.skip_tagged_list()

