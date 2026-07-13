


class JavaInternalProperty:
    """"""

    def __init__(self, native):
        self._native = native


    @property
    def app_context(self):
        """"""
        return self._native.app_context


