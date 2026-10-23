//

//

import Foundation

/// Cpp is included for methods that need a native implementation.
public class OnlyFunctions {


    public static let swiftConstant: Int32 = 33
    let c_instance : _baseRef

    init(cOnlyFunctions: _baseRef) {
        guard cOnlyFunctions != 0 else {
            fatalError("Nullptr value is not supported for initializers")
        }
        c_instance = cOnlyFunctions
    }

    deinit {
        smoke_OnlyFunctions_remove_swift_object_from_wrapper_cache(c_instance)
        smoke_OnlyFunctions_release_handle(c_instance)
    }

    ///
    /// - Parameter input: String to round trip through the native implementation.
    /// - Returns: The unchanged input.
    public static func swiftOnly(input: String) -> String {
        let c_input = moveToCType(input)
        let c_result_handle = smoke_OnlyFunctions_swiftOnly(c_input.ref)
        return moveFromCType(c_result_handle)
    }
    ///
    /// - Parameter input: String to round trip through the native implementation.
    /// - Returns: The unchanged input.
    public static func shared(input: String) -> String {
        let c_input = moveToCType(input)
        let c_result_handle = smoke_OnlyFunctions_shared(c_input.ref)
        return moveFromCType(c_result_handle)
    }

}



internal func getRef(_ ref: OnlyFunctions?, owning: Bool = true) -> RefHolder {
    guard let c_handle = ref?.c_instance else {
        return RefHolder(0)
    }
    let handle_copy = smoke_OnlyFunctions_copy_handle(c_handle)
    return owning
        ? RefHolder(ref: handle_copy, release: smoke_OnlyFunctions_release_handle)
        : RefHolder(handle_copy)
}

extension OnlyFunctions: NativeBase {
    /// :nodoc:
    var c_handle: _baseRef { return c_instance }
}
extension OnlyFunctions: Hashable {
    /// :nodoc:
    public static func == (lhs: OnlyFunctions, rhs: OnlyFunctions) -> Bool {
        return lhs.c_handle == rhs.c_handle
    }

    /// :nodoc:
    public func hash(into hasher: inout Hasher) {
        hasher.combine(c_handle)
    }
}

internal func OnlyFunctions_copyFromCType(_ handle: _baseRef) -> OnlyFunctions {
    if let swift_pointer = smoke_OnlyFunctions_get_swift_object_from_wrapper_cache(handle),
        let re_constructed = Unmanaged<AnyObject>.fromOpaque(swift_pointer).takeUnretainedValue() as? OnlyFunctions {
        return re_constructed
    }
    let result = OnlyFunctions(cOnlyFunctions: smoke_OnlyFunctions_copy_handle(handle))
    smoke_OnlyFunctions_cache_swift_object_wrapper(handle, Unmanaged<AnyObject>.passUnretained(result).toOpaque())
    return result
}

internal func OnlyFunctions_moveFromCType(_ handle: _baseRef) -> OnlyFunctions {
    if let swift_pointer = smoke_OnlyFunctions_get_swift_object_from_wrapper_cache(handle),
        let re_constructed = Unmanaged<AnyObject>.fromOpaque(swift_pointer).takeUnretainedValue() as? OnlyFunctions {
        smoke_OnlyFunctions_release_handle(handle)
        return re_constructed
    }
    let result = OnlyFunctions(cOnlyFunctions: handle)
    smoke_OnlyFunctions_cache_swift_object_wrapper(handle, Unmanaged<AnyObject>.passUnretained(result).toOpaque())
    return result
}

internal func OnlyFunctions_copyFromCType(_ handle: _baseRef) -> OnlyFunctions? {
    guard handle != 0 else {
        return nil
    }
    return OnlyFunctions_moveFromCType(handle) as OnlyFunctions
}
internal func OnlyFunctions_moveFromCType(_ handle: _baseRef) -> OnlyFunctions? {
    guard handle != 0 else {
        return nil
    }
    return OnlyFunctions_moveFromCType(handle) as OnlyFunctions
}

internal func copyToCType(_ swiftClass: OnlyFunctions) -> RefHolder {
    return getRef(swiftClass, owning: false)
}

internal func moveToCType(_ swiftClass: OnlyFunctions) -> RefHolder {
    return getRef(swiftClass, owning: true)
}

internal func copyToCType(_ swiftClass: OnlyFunctions?) -> RefHolder {
    return getRef(swiftClass, owning: false)
}

internal func moveToCType(_ swiftClass: OnlyFunctions?) -> RefHolder {
    return getRef(swiftClass, owning: true)
}
