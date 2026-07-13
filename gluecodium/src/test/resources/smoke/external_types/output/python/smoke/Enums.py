

from smoke.ExternalEnum import ExternalEnum

class Enums:
    """"""

    def __init__(self, native):
        self._native = native


    def method_with_external_enum(self, input: ExternalEnum):
        """"""
        return self._native.method_with_external_enum(input)

