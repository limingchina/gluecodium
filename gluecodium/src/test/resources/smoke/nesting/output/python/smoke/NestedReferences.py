

from smoke.NestedReferences import NestedReferences

class NestedReferences:
    """"""

    def __init__(self, native):
        self._native = native


    def inside_out(self, struct1: NestedReferences, struct2: NestedReferences) -> NestedReferences:
        """"""
        return self._native.inside_out(struct1, struct2)

