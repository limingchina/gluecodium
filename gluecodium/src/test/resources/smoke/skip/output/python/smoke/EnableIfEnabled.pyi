


from _native_base import _NativeBase


class EnableIfEnabled(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def enable_if_unquoted(self):
        """"""
        return self._native.enable_if_unquoted()


    def enable_if_unquoted_list(self):
        """"""
        return self._native.enable_if_unquoted_list()


    def enable_if_quoted(self):
        """"""
        return self._native.enable_if_quoted()


    def enable_if_quoted_list(self):
        """"""
        return self._native.enable_if_quoted_list()


    def enable_if_tagged(self):
        """"""
        return self._native.enable_if_tagged()


    def enable_if_tagged_list(self):
        """"""
        return self._native.enable_if_tagged_list()


    def enable_if_mixed_list(self):
        """"""
        return self._native.enable_if_mixed_list()

