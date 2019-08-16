//
//
// Automatically generated. Do not modify. Your changes will be lost.
import Foundation
@_cdecl("_CBridgeInitsmoke_SimpleClass")
internal func _CBridgeInitsmoke_SimpleClass(handle: _baseRef) -> UnsafeMutableRawPointer {
    let reference = SimpleClass(cSimpleClass: handle)
    return Unmanaged<AnyObject>.passRetained(reference).toOpaque()
}
internal func getRef(_ ref: SimpleClass?, owning: Bool = true) -> RefHolder {
    guard let c_handle = ref?.c_instance else {
        return RefHolder(0)
    }
    let handle_copy = smoke_SimpleClass_copy_handle(c_handle)
    return owning
        ? RefHolder(ref: handle_copy, release: smoke_SimpleClass_release_handle)
        : RefHolder(handle_copy)
}
public class SimpleClass {
    let c_instance : _baseRef
    init(cSimpleClass: _baseRef) {
        guard cSimpleClass != 0 else {
            fatalError("Nullptr value is not supported for initializers")
        }
        c_instance = cSimpleClass
    }
    deinit {
        smoke_SimpleClass_release_handle(c_instance)
    }
    public func getStringValue() -> String {
        return moveFromCType(smoke_SimpleClass_getStringValue(self.c_instance))
    }
}
extension SimpleClass: NativeBase {
    var c_handle: _baseRef { return c_instance }
}
internal func SimpleClasscopyFromCType(_ handle: _baseRef) -> SimpleClass {
    if let swift_pointer = smoke_SimpleClass_get_typed(smoke_SimpleClass_copy_handle(handle)),
        let typed = Unmanaged<AnyObject>.fromOpaque(swift_pointer).takeRetainedValue() as? SimpleClass {
        return typed
    }
    fatalError("Failed to initialize Swift object")
}
internal func SimpleClassmoveFromCType(_ handle: _baseRef) -> SimpleClass {
    if let swift_pointer = smoke_SimpleClass_get_typed(handle),
        let typed = Unmanaged<AnyObject>.fromOpaque(swift_pointer).takeRetainedValue() as? SimpleClass {
        return typed
    }
    fatalError("Failed to initialize Swift object")
}
internal func SimpleClasscopyFromCType(_ handle: _baseRef) -> SimpleClass? {
    guard handle != 0 else {
        return nil
    }
    return SimpleClassmoveFromCType(handle) as SimpleClass
}
internal func SimpleClassmoveFromCType(_ handle: _baseRef) -> SimpleClass? {
    guard handle != 0 else {
        return nil
    }
    return SimpleClassmoveFromCType(handle) as SimpleClass
}
internal func copyToCType(_ swiftClass: SimpleClass) -> RefHolder {
    return getRef(swiftClass, owning: false)
}
internal func moveToCType(_ swiftClass: SimpleClass) -> RefHolder {
    return getRef(swiftClass, owning: true)
}
internal func copyToCType(_ swiftClass: SimpleClass?) -> RefHolder {
    return getRef(swiftClass, owning: false)
}
internal func moveToCType(_ swiftClass: SimpleClass?) -> RefHolder {
    return getRef(swiftClass, owning: true)
}