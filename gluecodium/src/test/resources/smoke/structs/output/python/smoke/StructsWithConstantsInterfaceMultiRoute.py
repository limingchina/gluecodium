

from __future__ import annotations

from smoke.RouteUtilsRouteType import RouteUtilsRouteType


from _native_base import _NativeBase

import generated


class StructsWithConstantsInterfaceMultiRoute(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsWithConstantsInterfaceMultiRoute):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsWithConstantsInterfaceMultiRoute(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def descriptions(self) -> list[str]:
        """"""
        return self._native.descriptions
    @descriptions.setter
    def descriptions(self, value: list[str]):
      self._native.descriptions = getattr(value, "_native", value)



    @property
    def type(self) -> RouteUtilsRouteType:
        """"""
        return RouteUtilsRouteType(self._native.type)
    @type.setter
    def type(self, value: RouteUtilsRouteType):
      self._native.type = getattr(value, "_native", value)



    DEFAULT_DESCRIPTION = "Foo"


    DEFAULT_TYPE = RouteType.NONE

