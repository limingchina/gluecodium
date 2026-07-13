


class ParentNarrowOne:
    """"""

    def __init__(self, native):
        self._native = native


    def parent_function_one(self):
        """"""
        return self._native.parent_function_one()


    @property
    def parent_property_one(self) -> str:
        """"""
        return self._native.parent_property_one


