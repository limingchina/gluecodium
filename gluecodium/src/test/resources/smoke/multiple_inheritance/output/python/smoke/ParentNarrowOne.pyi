



from _native_base import _NativeBase

import generated


class ParentNarrowOne(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ParentNarrowOne):
            super().__init__(native)
        else:
            super().__init__(generated.ParentNarrowOne())


    def parent_function_one(self):
        """"""
        return self._native.parent_function_one()


    @property
    def parent_property_one(self) -> str:
        """"""
        return self._native.parent_property_one

    @parent_property_one.setter
    def parent_property_one(self, value: str):
        self._native.parent_property_one = value

