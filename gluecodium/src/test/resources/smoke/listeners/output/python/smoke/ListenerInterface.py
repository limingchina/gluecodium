


class ListenerInterface:
    """"""

    def __init__(self, native):
        self._native = native


    def notify(self):
        """"""
        return self._native.notify()

