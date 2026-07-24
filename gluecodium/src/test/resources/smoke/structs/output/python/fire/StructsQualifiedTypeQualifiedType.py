

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.StructsInstance import StructsInstance
from smoke.StructsPoint import StructsPoint
from smoke.TypeCollectionPoint import TypeCollectionPoint


from _native_base import _NativeBase

import generated


class StructsQualifiedTypeQualifiedType(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsQualifiedTypeQualifiedType):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsQualifiedTypeQualifiedType(*[_unwrap(arg) for arg in args]))


    @property
    def type_collection_point(self) -> TypeCollectionPoint:
        """"""
        return _wrap(self._native.type_collection_point, TypeCollectionPoint)
    @type_collection_point.setter
    def type_collection_point(self, value: TypeCollectionPoint):
      self._native.type_collection_point = _unwrap(value, TypeCollectionPoint)



    @property
    def interface_point(self) -> StructsPoint:
        """"""
        return _wrap(self._native.interface_point, StructsPoint)
    @interface_point.setter
    def interface_point(self, value: StructsPoint):
      self._native.interface_point = _unwrap(value, StructsPoint)



    @property
    def type_collection_explicit_points(self) -> list[StructsPoint]:
        """"""
        return _wrap(self._native.type_collection_explicit_points, list[StructsPoint])
    @type_collection_explicit_points.setter
    def type_collection_explicit_points(self, value: list[StructsPoint]):
      self._native.type_collection_explicit_points = _unwrap(value, list[StructsPoint])



    @property
    def interface_explicit_points(self) -> list[StructsPoint]:
        """"""
        return _wrap(self._native.interface_explicit_points, list[StructsPoint])
    @interface_explicit_points.setter
    def interface_explicit_points(self, value: list[StructsPoint]):
      self._native.interface_explicit_points = _unwrap(value, list[StructsPoint])



    @property
    def type_collection_implicit_points(self) -> list[TypeCollectionPoint]:
        """"""
        return _wrap(self._native.type_collection_implicit_points, list[TypeCollectionPoint])
    @type_collection_implicit_points.setter
    def type_collection_implicit_points(self, value: list[TypeCollectionPoint]):
      self._native.type_collection_implicit_points = _unwrap(value, list[TypeCollectionPoint])



    @property
    def interface_implicit_points(self) -> list[StructsPoint]:
        """"""
        return _wrap(self._native.interface_implicit_points, list[StructsPoint])
    @interface_implicit_points.setter
    def interface_implicit_points(self, value: list[StructsPoint]):
      self._native.interface_implicit_points = _unwrap(value, list[StructsPoint])



    @property
    def structs_instance(self) -> StructsInstance:
        """"""
        return _wrap(self._native.structs_instance, StructsInstance)
    @structs_instance.setter
    def structs_instance(self, value: StructsInstance):
      self._native.structs_instance = _unwrap(value, StructsInstance)


