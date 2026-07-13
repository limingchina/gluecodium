



from _native_base import _NativeBase

import generated


class NestedReferences(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def inside_out(self, struct1: NestedReferences, struct2: NestedReferences) -> NestedReferences:
        """"""
        return self._native.inside_out(struct1._native, struct2._native)

