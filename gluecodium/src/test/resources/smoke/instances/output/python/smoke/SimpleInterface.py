

from smoke.SimpleInterface import SimpleInterface

class SimpleInterface:
    """"""

    def __init__(self, native):
        self._native = native


    def get_string_value(self) -> str:
        """"""
        return self._native.get_string_value()


    def use_simple_interface(self, input: SimpleInterface) -> SimpleInterface:
        """"""
        return self._native.use_simple_interface(input)

