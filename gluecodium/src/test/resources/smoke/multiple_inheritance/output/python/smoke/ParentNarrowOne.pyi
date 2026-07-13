


from _native_base import _NativeBase


class ParentNarrowOne(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def parent_function_one(self):
        """"""
        return self._native.parent_function_one()


    @property
    def parent_property_one(self) -> str:
        """"""
        return self._native.parent_property_one


