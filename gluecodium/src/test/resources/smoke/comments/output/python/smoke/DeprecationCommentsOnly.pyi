

import typing

class DeprecationCommentsOnly:
    """"""

    def some_method_with_all_comments(self, input: str) -> bool:
        """"""
        ...

    @property
    def is_some_property(self) -> bool:
        """"""
        ...

    @is_some_property.setter
    def is_some_property(self, value: bool) -> None:
        ...

    #: 
    VERY_USEFUL = True

