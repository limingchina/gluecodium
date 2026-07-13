


class ParentNarrowTwo:
    """"""

    def __init__(self, native):
        self._native = native


    def parent_function_two(self):
        """"""
        return self._native.parent_function_two()


    @property
    def parent_property_two(self) -> str:
        """"""
        return self._native.parent_property_two


