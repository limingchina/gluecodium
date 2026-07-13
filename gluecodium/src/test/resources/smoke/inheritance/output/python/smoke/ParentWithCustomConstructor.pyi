



from _native_base import _NativeBase

import generated


class ParentWithCustomConstructor(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def create() -> ParentWithCustomConstructor:
        """"""
        native_result = generated.ParentWithCustomConstructor.create()
        return ParentWithCustomConstructor(native_result)

