

from smoke.SimpleClass import SimpleClass

class SimpleClass:
    """"""

    def __init__(self, native):
        self._native = native


    def get_string_value(self) -> str:
        """"""
        return self._native.get_string_value()


    def use_simple_class(self, input: SimpleClass) -> SimpleClass:
        """"""
        return self._native.use_simple_class(input)

