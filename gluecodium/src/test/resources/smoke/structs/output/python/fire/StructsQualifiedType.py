

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.Structs import Structs
from smoke.StructsInstance import StructsInstance
from smoke.TypeCollection import TypeCollection

class StructsQualifiedType(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    class QualifiedType(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.fire_StructsQualifiedTypeQualifiedType):
                super().__init__(args[0])
            else:
                super().__init__(generated.fire_StructsQualifiedTypeQualifiedType(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def type_collection_point(self) -> TypeCollection.Point:
            return _wrap(self._native.type_collection_point, TypeCollection.Point)
        @type_collection_point.setter
        def type_collection_point(self, value: TypeCollection.Point):
          self._native.type_collection_point = _unwrap(value, TypeCollection.Point)
    
    
        @property
        def interface_point(self) -> Structs.Point:
            return _wrap(self._native.interface_point, Structs.Point)
        @interface_point.setter
        def interface_point(self, value: Structs.Point):
          self._native.interface_point = _unwrap(value, Structs.Point)
    
    
        @property
        def type_collection_explicit_points(self) -> list[Structs.Point]:
            return _wrap(self._native.type_collection_explicit_points, list[Structs.Point])
        @type_collection_explicit_points.setter
        def type_collection_explicit_points(self, value: list[Structs.Point]):
          self._native.type_collection_explicit_points = _unwrap(value, list[Structs.Point])
    
    
        @property
        def interface_explicit_points(self) -> list[Structs.Point]:
            return _wrap(self._native.interface_explicit_points, list[Structs.Point])
        @interface_explicit_points.setter
        def interface_explicit_points(self, value: list[Structs.Point]):
          self._native.interface_explicit_points = _unwrap(value, list[Structs.Point])
    
    
        @property
        def type_collection_implicit_points(self) -> list[TypeCollection.Point]:
            return _wrap(self._native.type_collection_implicit_points, list[TypeCollection.Point])
        @type_collection_implicit_points.setter
        def type_collection_implicit_points(self, value: list[TypeCollection.Point]):
          self._native.type_collection_implicit_points = _unwrap(value, list[TypeCollection.Point])
    
    
        @property
        def interface_implicit_points(self) -> list[Structs.Point]:
            return _wrap(self._native.interface_implicit_points, list[Structs.Point])
        @interface_implicit_points.setter
        def interface_implicit_points(self, value: list[Structs.Point]):
          self._native.interface_implicit_points = _unwrap(value, list[Structs.Point])
    
    
        @property
        def structs_instance(self) -> StructsInstance:
            return _wrap(self._native.structs_instance, StructsInstance)
        @structs_instance.setter
        def structs_instance(self, value: StructsInstance):
          self._native.structs_instance = _unwrap(value, StructsInstance)
    
    
    
    
    list[Structs.Point] = list[Structs.Point]
    
    
    
    list[Structs.Point] = list[Structs.Point]
    
    

