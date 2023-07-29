//

//

import Foundation

/// Test class for cross reference of enum values without under score. Always working.
public class TestClassEnumValueWithoutUnderScore {


    let c_instance : _baseRef

    init(cTestClassEnumValueWithoutUnderScore: _baseRef) {
        guard cTestClassEnumValueWithoutUnderScore != 0 else {
            fatalError("Nullptr value is not supported for initializers")
        }
        c_instance = cTestClassEnumValueWithoutUnderScore
    }

    deinit {
        test_TestClassEnumValueWithoutUnderScore_remove_swift_object_from_wrapper_cache(c_instance)
        test_TestClassEnumValueWithoutUnderScore_release_handle(c_instance)
    }

    /// Note:a `Error.internal` error is generated.
    public func fooGoodCase() -> Void {
        test_TestClassEnumValueWithoutUnderScore_fooGoodCase(self.c_instance)
    }
    /// *Note: `Error.internal` error is generated.
    public func fooStarGoodCase1() -> Void {
        test_TestClassEnumValueWithoutUnderScore_fooStarGoodCase1(self.c_instance)
    }
    /// Note:* `Error.internal` error is generated.
    public func fooStarGoodCase2() -> Void {
        test_TestClassEnumValueWithoutUnderScore_fooStarGoodCase2(self.c_instance)
    }
    /// This is a test
    ///
    /// **Note:** `Error.internal` is generated.
    public func fooSentenceWithANewLineGoodCase() -> Void {
        test_TestClassEnumValueWithoutUnderScore_fooSentenceWithANewLineGoodCase(self.c_instance)
    }
    /// This is a tes
    ///
    /// **Note:** `Error.internal` is generated.
    public func fooShorterSentenceWithANewLineGoodCase() -> Void {
        test_TestClassEnumValueWithoutUnderScore_fooShorterSentenceWithANewLineGoodCase(self.c_instance)
    }

}



internal func getRef(_ ref: TestClassEnumValueWithoutUnderScore?, owning: Bool = true) -> RefHolder {
    guard let c_handle = ref?.c_instance else {
        return RefHolder(0)
    }
    let handle_copy = test_TestClassEnumValueWithoutUnderScore_copy_handle(c_handle)
    return owning
        ? RefHolder(ref: handle_copy, release: test_TestClassEnumValueWithoutUnderScore_release_handle)
        : RefHolder(handle_copy)
}

extension TestClassEnumValueWithoutUnderScore: NativeBase {
    /// :nodoc:
    var c_handle: _baseRef { return c_instance }
}
extension TestClassEnumValueWithoutUnderScore: Hashable {
    /// :nodoc:
    public static func == (lhs: TestClassEnumValueWithoutUnderScore, rhs: TestClassEnumValueWithoutUnderScore) -> Bool {
        return lhs.c_handle == rhs.c_handle
    }

    /// :nodoc:
    public func hash(into hasher: inout Hasher) {
        hasher.combine(c_handle)
    }
}

internal func TestClassEnumValueWithoutUnderScore_copyFromCType(_ handle: _baseRef) -> TestClassEnumValueWithoutUnderScore {
    if let swift_pointer = test_TestClassEnumValueWithoutUnderScore_get_swift_object_from_wrapper_cache(handle),
        let re_constructed = Unmanaged<AnyObject>.fromOpaque(swift_pointer).takeUnretainedValue() as? TestClassEnumValueWithoutUnderScore {
        return re_constructed
    }
    let result = TestClassEnumValueWithoutUnderScore(cTestClassEnumValueWithoutUnderScore: test_TestClassEnumValueWithoutUnderScore_copy_handle(handle))
    test_TestClassEnumValueWithoutUnderScore_cache_swift_object_wrapper(handle, Unmanaged<AnyObject>.passUnretained(result).toOpaque())
    return result
}

internal func TestClassEnumValueWithoutUnderScore_moveFromCType(_ handle: _baseRef) -> TestClassEnumValueWithoutUnderScore {
    if let swift_pointer = test_TestClassEnumValueWithoutUnderScore_get_swift_object_from_wrapper_cache(handle),
        let re_constructed = Unmanaged<AnyObject>.fromOpaque(swift_pointer).takeUnretainedValue() as? TestClassEnumValueWithoutUnderScore {
        test_TestClassEnumValueWithoutUnderScore_release_handle(handle)
        return re_constructed
    }
    let result = TestClassEnumValueWithoutUnderScore(cTestClassEnumValueWithoutUnderScore: handle)
    test_TestClassEnumValueWithoutUnderScore_cache_swift_object_wrapper(handle, Unmanaged<AnyObject>.passUnretained(result).toOpaque())
    return result
}

internal func TestClassEnumValueWithoutUnderScore_copyFromCType(_ handle: _baseRef) -> TestClassEnumValueWithoutUnderScore? {
    guard handle != 0 else {
        return nil
    }
    return TestClassEnumValueWithoutUnderScore_moveFromCType(handle) as TestClassEnumValueWithoutUnderScore
}
internal func TestClassEnumValueWithoutUnderScore_moveFromCType(_ handle: _baseRef) -> TestClassEnumValueWithoutUnderScore? {
    guard handle != 0 else {
        return nil
    }
    return TestClassEnumValueWithoutUnderScore_moveFromCType(handle) as TestClassEnumValueWithoutUnderScore
}

internal func copyToCType(_ swiftClass: TestClassEnumValueWithoutUnderScore) -> RefHolder {
    return getRef(swiftClass, owning: false)
}

internal func moveToCType(_ swiftClass: TestClassEnumValueWithoutUnderScore) -> RefHolder {
    return getRef(swiftClass, owning: true)
}

internal func copyToCType(_ swiftClass: TestClassEnumValueWithoutUnderScore?) -> RefHolder {
    return getRef(swiftClass, owning: false)
}

internal func moveToCType(_ swiftClass: TestClassEnumValueWithoutUnderScore?) -> RefHolder {
    return getRef(swiftClass, owning: true)
}



