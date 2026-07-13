

from smoke.ParentWithCustomConstructor import ParentWithCustomConstructor


from _native_base import _NativeBase

import generated


class ChildWithCustomConstructor(
    ParentWithCustomConstructor)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def make() -> ChildWithCustomConstructor:
        """"""
        native_result = generated.ChildWithCustomConstructor.make()
        return ChildWithCustomConstructor(native_result)

