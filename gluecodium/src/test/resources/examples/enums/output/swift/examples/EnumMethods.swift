//
//
import Foundation
public class EnumMethods {
    let c_instance : _baseRef
    init(cEnumMethods: _baseRef) {
        guard cEnumMethods != 0 else {
            fatalError("Nullptr value is not supported for initializers")
        }
        c_instance = cEnumMethods
    }
    deinit {
        examples_EnumMethods_release_handle(c_instance)
    }
    public static func methodWithEnumeration(input: ShoeSizes) -> ShoeSizes {
        let c_input = moveToCType(input)
        return moveFromCType(examples_EnumMethods_methodWithEnumeration(c_input.ref))
    }
}
internal func getRef(_ ref: EnumMethods?, owning: Bool = true) -> RefHolder {
    guard let c_handle = ref?.c_instance else {
        return RefHolder(0)
    }
    let handle_copy = examples_EnumMethods_copy_handle(c_handle)
    return owning
        ? RefHolder(ref: handle_copy, release: examples_EnumMethods_release_handle)
        : RefHolder(handle_copy)
}
extension EnumMethods: NativeBase {
    var c_handle: _baseRef { return c_instance }
}
internal func EnumMethods_copyFromCType(_ handle: _baseRef) -> EnumMethods {
    return EnumMethods(cEnumMethods: examples_EnumMethods_copy_handle(handle))
}
internal func EnumMethods_moveFromCType(_ handle: _baseRef) -> EnumMethods {
    return EnumMethods(cEnumMethods: handle)
}
internal func EnumMethods_copyFromCType(_ handle: _baseRef) -> EnumMethods? {
    guard handle != 0 else {
        return nil
    }
    return EnumMethods_moveFromCType(handle) as EnumMethods
}
internal func EnumMethods_moveFromCType(_ handle: _baseRef) -> EnumMethods? {
    guard handle != 0 else {
        return nil
    }
    return EnumMethods_moveFromCType(handle) as EnumMethods
}
internal func copyToCType(_ swiftClass: EnumMethods) -> RefHolder {
    return getRef(swiftClass, owning: false)
}
internal func moveToCType(_ swiftClass: EnumMethods) -> RefHolder {
    return getRef(swiftClass, owning: true)
}
internal func copyToCType(_ swiftClass: EnumMethods?) -> RefHolder {
    return getRef(swiftClass, owning: false)
}
internal func moveToCType(_ swiftClass: EnumMethods?) -> RefHolder {
    return getRef(swiftClass, owning: true)
}