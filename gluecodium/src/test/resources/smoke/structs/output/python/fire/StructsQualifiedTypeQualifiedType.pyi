

from smoke.StructsInstance import StructsInstance
from smoke.StructsPoint import StructsPoint
from smoke.TypeCollectionPoint import TypeCollectionPoint
import typing

class StructsQualifiedTypeQualifiedType:

    type_collection_point: TypeCollectionPoint

    interface_point: StructsPoint

    type_collection_explicit_points: list[StructsPoint]

    interface_explicit_points: list[StructsPoint]

    type_collection_implicit_points: list[TypeCollectionPoint]

    interface_implicit_points: list[StructsPoint]

    structs_instance: StructsInstance

