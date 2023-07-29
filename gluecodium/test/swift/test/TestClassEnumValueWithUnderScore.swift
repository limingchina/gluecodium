//

//

import Foundation

/// Test class for cross references of enum values with under score. Some cases don't work.
public class TestClassEnumValueWithUnderScore {


    let c_instance : _baseRef

    init(cTestClassEnumValueWithUnderScore: _baseRef) {
        guard cTestClassEnumValueWithUnderScore != 0 else {
            fatalError("Nullptr value is not supported for initializers")
        }
        c_instance = cTestClassEnumValueWithUnderScore
    }

    deinit {
        test_TestClassEnumValueWithUnderScore_remove_swift_object_from_wrapper_cache(c_instance)
        test_TestClassEnumValueWithUnderScore_release_handle(c_instance)
    }

    /// Note:a `Error.invalidParameter` error is generated.
    public func fooGoodCase() -> Void {
        test_TestClassEnumValueWithUnderScore_fooGoodCase(self.c_instance)
    }
    /// Note:* [Error.INVALID_PARAMETER] error is generated.
    public func fooStarBadCase1() -> Void {
        test_TestClassEnumValueWithUnderScore_fooStarBadCase1(self.c_instance)
    }
    /// *Note: [Error.INVALID_PARAMETER] error is generated.
    public func fooStarBadCase2() -> Void {
        test_TestClassEnumValueWithUnderScore_fooStarBadCase2(self.c_instance)
    }
    /// This is a test
    ///
    /// *Note: `Error.invalidParameter` is generated.
    public func fooSentenceWithANewLineGoodCase() -> Void {
        test_TestClassEnumValueWithUnderScore_fooSentenceWithANewLineGoodCase(self.c_instance)
    }
    /// This is a tes
    ///
    /// *Note: [Error.INVALID_PARAMETER] is generated.
    public func fooShorterSentenceWithANewLineBadCase() -> Void {
        test_TestClassEnumValueWithUnderScore_fooShorterSentenceWithANewLineBadCase(self.c_instance)
    }

}



internal func getRef(_ ref: TestClassEnumValueWithUnderScore?, owning: Bool = true) -> RefHolder {
    guard let c_handle = ref?.c_instance else {
        return RefHolder(0)
    }
    let handle_copy = test_TestClassEnumValueWithUnderScore_copy_handle(c_handle)
    return owning
        ? RefHolder(ref: handle_copy, release: test_TestClassEnumValueWithUnderScore_release_handle)
        : RefHolder(handle_copy)
}

extension TestClassEnumValueWithUnderScore: NativeBase {
    /// :nodoc:
    var c_handle: _baseRef { return c_instance }
}
extension TestClassEnumValueWithUnderScore: Hashable {
    /// :nodoc:
    public static func == (lhs: TestClassEnumValueWithUnderScore, rhs: TestClassEnumValueWithUnderScore) -> Bool {
        return lhs.c_handle == rhs.c_handle
    }

    /// :nodoc:
    public func hash(into hasher: inout Hasher) {
        hasher.combine(c_handle)
    }
}

internal func TestClassEnumValueWithUnderScore_copyFromCType(_ handle: _baseRef) -> TestClassEnumValueWithUnderScore {
    if let swift_pointer = test_TestClassEnumValueWithUnderScore_get_swift_object_from_wrapper_cache(handle),
        let re_constructed = Unmanaged<AnyObject>.fromOpaque(swift_pointer).takeUnretainedValue() as? TestClassEnumValueWithUnderScore {
        return re_constructed
    }
    let result = TestClassEnumValueWithUnderScore(cTestClassEnumValueWithUnderScore: test_TestClassEnumValueWithUnderScore_copy_handle(handle))
    test_TestClassEnumValueWithUnderScore_cache_swift_object_wrapper(handle, Unmanaged<AnyObject>.passUnretained(result).toOpaque())
    return result
}

internal func TestClassEnumValueWithUnderScore_moveFromCType(_ handle: _baseRef) -> TestClassEnumValueWithUnderScore {
    if let swift_pointer = test_TestClassEnumValueWithUnderScore_get_swift_object_from_wrapper_cache(handle),
        let re_constructed = Unmanaged<AnyObject>.fromOpaque(swift_pointer).takeUnretainedValue() as? TestClassEnumValueWithUnderScore {
        test_TestClassEnumValueWithUnderScore_release_handle(handle)
        return re_constructed
    }
    let result = TestClassEnumValueWithUnderScore(cTestClassEnumValueWithUnderScore: handle)
    test_TestClassEnumValueWithUnderScore_cache_swift_object_wrapper(handle, Unmanaged<AnyObject>.passUnretained(result).toOpaque())
    return result
}

internal func TestClassEnumValueWithUnderScore_copyFromCType(_ handle: _baseRef) -> TestClassEnumValueWithUnderScore? {
    guard handle != 0 else {
        return nil
    }
    return TestClassEnumValueWithUnderScore_moveFromCType(handle) as TestClassEnumValueWithUnderScore
}
internal func TestClassEnumValueWithUnderScore_moveFromCType(_ handle: _baseRef) -> TestClassEnumValueWithUnderScore? {
    guard handle != 0 else {
        return nil
    }
    return TestClassEnumValueWithUnderScore_moveFromCType(handle) as TestClassEnumValueWithUnderScore
}

internal func copyToCType(_ swiftClass: TestClassEnumValueWithUnderScore) -> RefHolder {
    return getRef(swiftClass, owning: false)
}

internal func moveToCType(_ swiftClass: TestClassEnumValueWithUnderScore) -> RefHolder {
    return getRef(swiftClass, owning: true)
}

internal func copyToCType(_ swiftClass: TestClassEnumValueWithUnderScore?) -> RefHolder {
    return getRef(swiftClass, owning: false)
}

internal func moveToCType(_ swiftClass: TestClassEnumValueWithUnderScore?) -> RefHolder {
    return getRef(swiftClass, owning: true)
}



