//
//

import Foundation
internal func getRef(_ ref: GenericTypesWithGenericTypes?, owning: Bool = true) -> RefHolder {
    guard let c_handle = ref?.c_instance else {
        return RefHolder(0)
    }
    let handle_copy = smoke_GenericTypesWithGenericTypes_copy_handle(c_handle)
    return owning
        ? RefHolder(ref: handle_copy, release: smoke_GenericTypesWithGenericTypes_release_handle)
        : RefHolder(handle_copy)
}
public class GenericTypesWithGenericTypes {
    let c_instance : _baseRef
    init(cGenericTypesWithGenericTypes: _baseRef) {
        guard cGenericTypesWithGenericTypes != 0 else {
            fatalError("Nullptr value is not supported for initializers")
        }
        c_instance = cGenericTypesWithGenericTypes
    }
    deinit {
        smoke_GenericTypesWithGenericTypes_release_handle(c_instance)
    }
    public func methodWithListOfLists(input: [[Int32]]) -> [[Int32]] {
        let c_input = moveToCType(input)
        return moveFromCType(smoke_GenericTypesWithGenericTypes_methodWithListOfLists(self.c_instance, c_input.ref))
    }
    public func methodWithMapOfMaps(input: [Int32: [Int32: Bool]]) -> [[Int32: Bool]: Bool] {
        let c_input = moveToCType(input)
        return moveFromCType(smoke_GenericTypesWithGenericTypes_methodWithMapOfMaps(self.c_instance, c_input.ref))
    }
    public func methodWithSetOfSets(input: Set<Set<Int32>>) -> Set<Set<Int32>> {
        let c_input = moveToCType(input)
        return moveFromCType(smoke_GenericTypesWithGenericTypes_methodWithSetOfSets(self.c_instance, c_input.ref))
    }
    public func methodWithListAndMap(input: [[Int32: Bool]]) -> [Int32: [Int32]] {
        let c_input = moveToCType(input)
        return moveFromCType(smoke_GenericTypesWithGenericTypes_methodWithListAndMap(self.c_instance, c_input.ref))
    }
    public func methodWithListAndSet(input: [Set<Int32>]) -> Set<[Int32]> {
        let c_input = moveToCType(input)
        return moveFromCType(smoke_GenericTypesWithGenericTypes_methodWithListAndSet(self.c_instance, c_input.ref))
    }
    public func methodWithMapAndSet(input: [Int32: Set<Int32>]) -> Set<[Int32: Bool]> {
        let c_input = moveToCType(input)
        return moveFromCType(smoke_GenericTypesWithGenericTypes_methodWithMapAndSet(self.c_instance, c_input.ref))
    }
    public func methodWithMapGenericKeys(input: [Set<Int32>: Bool]) -> [[Int32]: Bool] {
        let c_input = moveToCType(input)
        return moveFromCType(smoke_GenericTypesWithGenericTypes_methodWithMapGenericKeys(self.c_instance, c_input.ref))
    }
}
extension GenericTypesWithGenericTypes: NativeBase {
    var c_handle: _baseRef { return c_instance }
}
internal func GenericTypesWithGenericTypescopyFromCType(_ handle: _baseRef) -> GenericTypesWithGenericTypes {
    return GenericTypesWithGenericTypes(cGenericTypesWithGenericTypes: smoke_GenericTypesWithGenericTypes_copy_handle(handle))
}
internal func GenericTypesWithGenericTypesmoveFromCType(_ handle: _baseRef) -> GenericTypesWithGenericTypes {
    return GenericTypesWithGenericTypes(cGenericTypesWithGenericTypes: handle)
}
internal func GenericTypesWithGenericTypescopyFromCType(_ handle: _baseRef) -> GenericTypesWithGenericTypes? {
    guard handle != 0 else {
        return nil
    }
    return GenericTypesWithGenericTypesmoveFromCType(handle) as GenericTypesWithGenericTypes
}
internal func GenericTypesWithGenericTypesmoveFromCType(_ handle: _baseRef) -> GenericTypesWithGenericTypes? {
    guard handle != 0 else {
        return nil
    }
    return GenericTypesWithGenericTypesmoveFromCType(handle) as GenericTypesWithGenericTypes
}
internal func copyToCType(_ swiftClass: GenericTypesWithGenericTypes) -> RefHolder {
    return getRef(swiftClass, owning: false)
}
internal func moveToCType(_ swiftClass: GenericTypesWithGenericTypes) -> RefHolder {
    return getRef(swiftClass, owning: true)
}
internal func copyToCType(_ swiftClass: GenericTypesWithGenericTypes?) -> RefHolder {
    return getRef(swiftClass, owning: false)
}
internal func moveToCType(_ swiftClass: GenericTypesWithGenericTypes?) -> RefHolder {
    return getRef(swiftClass, owning: true)
}
