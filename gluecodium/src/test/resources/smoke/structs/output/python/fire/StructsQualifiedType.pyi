

from smoke.Structs import Structs
from smoke.StructsInstance import StructsInstance
from smoke.TypeCollection import TypeCollection
from enum import Enum
import typing

class StructsQualifiedType:

    class QualifiedType:
    
        type_collection_point: TypeCollection.Point
    
        interface_point: Structs.Point
    
        type_collection_explicit_points: list[Structs.Point]
    
        interface_explicit_points: list[Structs.Point]
    
        type_collection_implicit_points: list[TypeCollection.Point]
    
        interface_implicit_points: list[Structs.Point]
    
        structs_instance: StructsInstance
    
    
    
    TypeCollectionPointsArray = list[Structs.Point]
    
    
    
    InterfacePointsArray = list[Structs.Point]
    
    

