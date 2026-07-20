

from smoke.StructsInstance import StructsInstance
from smoke.StructsPoint import StructsPoint
from smoke.TypeCollectionPoint import TypeCollectionPoint
import typing


from _native_base import _NativeBase

import generated


class StructsQualifiedTypeQualifiedType(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsQualifiedTypeQualifiedType):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsQualifiedTypeQualifiedType(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def type_collection_point(self) -> TypeCollectionPoint:
        """"""
        return TypeCollectionPoint(self._native.type_collection_point)
    @type_collection_point.setter
    def type_collection_point(self, value: TypeCollectionPoint):
      self._native.type_collection_point = getattr(value, "_native", value)



    @property
    def interface_point(self) -> StructsPoint:
        """"""
        return StructsPoint(self._native.interface_point)
    @interface_point.setter
    def interface_point(self, value: StructsPoint):
      self._native.interface_point = getattr(value, "_native", value)



    @property
    def type_collection_explicit_points(self) -> list[StructsPoint]:
        """"""
        return self._native.type_collection_explicit_points
    @type_collection_explicit_points.setter
    def type_collection_explicit_points(self, value: list[StructsPoint]):
      self._native.type_collection_explicit_points = getattr(value, "_native", value)



    @property
    def interface_explicit_points(self) -> list[StructsPoint]:
        """"""
        return self._native.interface_explicit_points
    @interface_explicit_points.setter
    def interface_explicit_points(self, value: list[StructsPoint]):
      self._native.interface_explicit_points = getattr(value, "_native", value)



    @property
    def type_collection_implicit_points(self) -> list[TypeCollectionPoint]:
        """"""
        return self._native.type_collection_implicit_points
    @type_collection_implicit_points.setter
    def type_collection_implicit_points(self, value: list[TypeCollectionPoint]):
      self._native.type_collection_implicit_points = getattr(value, "_native", value)



    @property
    def interface_implicit_points(self) -> list[StructsPoint]:
        """"""
        return self._native.interface_implicit_points
    @interface_implicit_points.setter
    def interface_implicit_points(self, value: list[StructsPoint]):
      self._native.interface_implicit_points = getattr(value, "_native", value)



    @property
    def structs_instance(self) -> StructsInstance:
        """"""
        return StructsInstance(self._native.structs_instance)
    @structs_instance.setter
    def structs_instance(self, value: StructsInstance):
      self._native.structs_instance = getattr(value, "_native", value)


