


from _native_base import _NativeBase


class ParentNarrowTwo(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def parent_function_two(self):
        """"""
        return self._native.parent_function_two()


    @property
    def parent_property_two(self) -> str:
        """"""
        return self._native.parent_property_two


