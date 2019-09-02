//
//

import Foundation
internal func getRef(_ ref: StructsWithConstantsInterface?, owning: Bool = true) -> RefHolder {
    guard let c_handle = ref?.c_instance else {
        return RefHolder(0)
    }
    let handle_copy = smoke_StructsWithConstantsInterface_copy_handle(c_handle)
    return owning
        ? RefHolder(ref: handle_copy, release: smoke_StructsWithConstantsInterface_release_handle)
        : RefHolder(handle_copy)
}
public class StructsWithConstantsInterface {
    let c_instance : _baseRef
    init(cStructsWithConstantsInterface: _baseRef) {
        guard cStructsWithConstantsInterface != 0 else {
            fatalError("Nullptr value is not supported for initializers")
        }
        c_instance = cStructsWithConstantsInterface
    }
    deinit {
        smoke_StructsWithConstantsInterface_release_handle(c_instance)
    }
    public struct MultiRoute {
        public static let defaultDescription: String = "Foo"
        public static let defaultType: RouteType = RouteType.none
        public var descriptions: [String]
        public var type: RouteType
        public init(descriptions: [String], type: RouteType) {
            self.descriptions = descriptions
            self.type = type
        }
        internal init(cHandle: _baseRef) {
            descriptions = moveFromCType(smoke_StructsWithConstantsInterface_MultiRoute_descriptions_get(cHandle))
            type = moveFromCType(smoke_StructsWithConstantsInterface_MultiRoute_type_get(cHandle))
        }
    }
}
extension StructsWithConstantsInterface: NativeBase {
    var c_handle: _baseRef { return c_instance }
}
internal func StructsWithConstantsInterfacecopyFromCType(_ handle: _baseRef) -> StructsWithConstantsInterface {
    return StructsWithConstantsInterface(cStructsWithConstantsInterface: smoke_StructsWithConstantsInterface_copy_handle(handle))
}
internal func StructsWithConstantsInterfacemoveFromCType(_ handle: _baseRef) -> StructsWithConstantsInterface {
    return StructsWithConstantsInterface(cStructsWithConstantsInterface: handle)
}
internal func StructsWithConstantsInterfacecopyFromCType(_ handle: _baseRef) -> StructsWithConstantsInterface? {
    guard handle != 0 else {
        return nil
    }
    return StructsWithConstantsInterfacemoveFromCType(handle) as StructsWithConstantsInterface
}
internal func StructsWithConstantsInterfacemoveFromCType(_ handle: _baseRef) -> StructsWithConstantsInterface? {
    guard handle != 0 else {
        return nil
    }
    return StructsWithConstantsInterfacemoveFromCType(handle) as StructsWithConstantsInterface
}
internal func copyToCType(_ swiftClass: StructsWithConstantsInterface) -> RefHolder {
    return getRef(swiftClass, owning: false)
}
internal func moveToCType(_ swiftClass: StructsWithConstantsInterface) -> RefHolder {
    return getRef(swiftClass, owning: true)
}
internal func copyToCType(_ swiftClass: StructsWithConstantsInterface?) -> RefHolder {
    return getRef(swiftClass, owning: false)
}
internal func moveToCType(_ swiftClass: StructsWithConstantsInterface?) -> RefHolder {
    return getRef(swiftClass, owning: true)
}
internal func copyFromCType(_ handle: _baseRef) -> StructsWithConstantsInterface.MultiRoute {
    return StructsWithConstantsInterface.MultiRoute(cHandle: handle)
}
internal func moveFromCType(_ handle: _baseRef) -> StructsWithConstantsInterface.MultiRoute {
    defer {
        smoke_StructsWithConstantsInterface_MultiRoute_release_handle(handle)
    }
    return copyFromCType(handle)
}
internal func copyToCType(_ swiftType: StructsWithConstantsInterface.MultiRoute) -> RefHolder {
    let c_descriptions = moveToCType(swiftType.descriptions)
    let c_type = moveToCType(swiftType.type)
    return RefHolder(smoke_StructsWithConstantsInterface_MultiRoute_create_handle(c_descriptions.ref, c_type.ref))
}
internal func moveToCType(_ swiftType: StructsWithConstantsInterface.MultiRoute) -> RefHolder {
    return RefHolder(ref: copyToCType(swiftType).ref, release: smoke_StructsWithConstantsInterface_MultiRoute_release_handle)
}
internal func copyFromCType(_ handle: _baseRef) -> StructsWithConstantsInterface.MultiRoute? {
    guard handle != 0 else {
        return nil
    }
    let unwrappedHandle = smoke_StructsWithConstantsInterface_MultiRoute_unwrap_optional_handle(handle)
    return StructsWithConstantsInterface.MultiRoute(cHandle: unwrappedHandle) as StructsWithConstantsInterface.MultiRoute
}
internal func moveFromCType(_ handle: _baseRef) -> StructsWithConstantsInterface.MultiRoute? {
    defer {
        smoke_StructsWithConstantsInterface_MultiRoute_release_optional_handle(handle)
    }
    return copyFromCType(handle)
}
internal func copyToCType(_ swiftType: StructsWithConstantsInterface.MultiRoute?) -> RefHolder {
    guard let swiftType = swiftType else {
        return RefHolder(0)
    }
    let c_descriptions = moveToCType(swiftType.descriptions)
    let c_type = moveToCType(swiftType.type)
    return RefHolder(smoke_StructsWithConstantsInterface_MultiRoute_create_optional_handle(c_descriptions.ref, c_type.ref))
}
internal func moveToCType(_ swiftType: StructsWithConstantsInterface.MultiRoute?) -> RefHolder {
    return RefHolder(ref: copyToCType(swiftType).ref, release: smoke_StructsWithConstantsInterface_MultiRoute_release_optional_handle)
}
