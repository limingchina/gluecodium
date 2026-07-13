

from smoke.Callback import Callback

class SpecialNamesInterface:
    """"""

    def __init__(self, native):
        self._native = native


    def dispatch(self, callback: Callback):
        """"""
        return self._native.dispatch(callback)

