

from smoke.RouteUtilsRouteType import RouteUtilsRouteType
import typing


from _native_base import _NativeBase

import generated


class StructsWithConstantsInterfaceMultiRoute(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_StructsWithConstantsInterfaceMultiRoute):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsWithConstantsInterfaceMultiRoute(*[_unwrap(arg) for arg in args]))


    @property
    def descriptions(self) -> list[str]:
        """"""
        return _wrap(self._native.descriptions, list[str])
    @descriptions.setter
    def descriptions(self, value: list[str]):
      self._native.descriptions = _unwrap(value, list[str])



    @property
    def type(self) -> RouteUtilsRouteType:
        """"""
        return _wrap(self._native.type, RouteUtilsRouteType)
    @type.setter
    def type(self, value: RouteUtilsRouteType):
      self._native.type = _unwrap(value, RouteUtilsRouteType)



    DEFAULT_DESCRIPTION = "Foo"


    DEFAULT_TYPE = RouteType.NONE

