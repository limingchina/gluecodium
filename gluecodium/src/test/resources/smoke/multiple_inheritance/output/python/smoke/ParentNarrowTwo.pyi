



from _native_base import _NativeBase

import generated


class ParentNarrowTwo(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ParentNarrowTwo):
            super().__init__(native)
        else:
            super().__init__(generated.ParentNarrowTwo())


    def parent_function_two(self):
        """"""
        return self._native.parent_function_two()


    @property
    def parent_property_two(self) -> str:
        """"""
        return self._native.parent_property_two

    @parent_property_two.setter
    def parent_property_two(self, value: str):
        self._native.parent_property_two = value

