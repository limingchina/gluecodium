


class AsyncWithSkips:
    """"""

    def __init__(self, native):
        self._native = native


    def make_shared_instance(self, android_context: str):
        """"""
        return self._native.make_shared_instance(android_context)


    def make_shared_instance(self):
        """"""
        return self._native.make_shared_instance()

