


class InternalListener:
    """"""

    def __init__(self, native):
        self._native = native


    def on_event(self):
        """"""
        return self._native.on_event()

