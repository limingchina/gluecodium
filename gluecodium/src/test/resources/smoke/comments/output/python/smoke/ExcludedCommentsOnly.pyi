

from smoke.ExcludedCommentsOnlySomeEnum import ExcludedCommentsOnlySomeEnum
from smoke.ExcludedCommentsOnlySomethingWrong import ExcludedCommentsOnlySomethingWrong
import typing

class ExcludedCommentsOnly:
    """"""

    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """"""
        ...

    def some_method_without_return_type_or_input_parameters(self):
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

