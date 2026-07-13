

from smoke.ListenerInterface import ListenerInterface

class Weakling:
    """"""

    def __init__(self, native):
        self._native = native


    @property
    def listener(self):
        """"""
        return self._native.listener


