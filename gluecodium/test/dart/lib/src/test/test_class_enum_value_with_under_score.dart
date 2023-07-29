

import 'dart:ffi';
import 'package:library/src/_library_context.dart' as __lib;
import 'package:library/src/_native_base.dart' as __lib;
import 'package:library/src/_token_cache.dart' as __lib;

/// Test class for cross references of enum values with under score.
///
/// Some cases don't work.
abstract class TestClassEnumValueWithUnderScore {

  /// Note:a [Error.invalidParameter] error is generated.
  ///
  void fooGoodCase();
  /// Note:* [Error.INVALID_PARAMETER] error is generated.
  ///
  void fooStarBadCase1();
  /// *Note: [Error.INVALID_PARAMETER] error is generated.
  ///
  void fooStarBadCase2();
  /// This is a test
  ///
  /// *Note: [Error.invalidParameter] is generated.
  ///
  void fooSentenceWithANewLineGoodCase();
  /// This is a tes
  ///
  /// *Note: [Error.INVALID_PARAMETER] is generated.
  ///
  void fooShorterSentenceWithANewLineBadCase();
}


// TestClassEnumValueWithUnderScore "private" section, not exported.

final _testTestclassenumvaluewithunderscoreRegisterFinalizer = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Void Function(Pointer<Void>, Int32, Handle),
    void Function(Pointer<Void>, int, Object)
  >('library_test_TestClassEnumValueWithUnderScore_register_finalizer'));
final _testTestclassenumvaluewithunderscoreCopyHandle = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_test_TestClassEnumValueWithUnderScore_copy_handle'));
final _testTestclassenumvaluewithunderscoreReleaseHandle = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Void Function(Pointer<Void>),
    void Function(Pointer<Void>)
  >('library_test_TestClassEnumValueWithUnderScore_release_handle'));







class TestClassEnumValueWithUnderScore$Impl extends __lib.NativeBase implements TestClassEnumValueWithUnderScore {

  TestClassEnumValueWithUnderScore$Impl(Pointer<Void> handle) : super(handle);

  @override
  void fooGoodCase() {
    final _fooGoodCaseFfi = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<Void Function(Pointer<Void>, Int32), void Function(Pointer<Void>, int)>('library_test_TestClassEnumValueWithUnderScore_fooGoodCase'));
    final _handle = this.handle;
    _fooGoodCaseFfi(_handle, __lib.LibraryContext.isolateId);

  }

  @override
  void fooStarBadCase1() {
    final _fooStarBadCase1Ffi = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<Void Function(Pointer<Void>, Int32), void Function(Pointer<Void>, int)>('library_test_TestClassEnumValueWithUnderScore_fooStarBadCase1'));
    final _handle = this.handle;
    _fooStarBadCase1Ffi(_handle, __lib.LibraryContext.isolateId);

  }

  @override
  void fooStarBadCase2() {
    final _fooStarBadCase2Ffi = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<Void Function(Pointer<Void>, Int32), void Function(Pointer<Void>, int)>('library_test_TestClassEnumValueWithUnderScore_fooStarBadCase2'));
    final _handle = this.handle;
    _fooStarBadCase2Ffi(_handle, __lib.LibraryContext.isolateId);

  }

  @override
  void fooSentenceWithANewLineGoodCase() {
    final _fooSentenceWithANewLineGoodCaseFfi = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<Void Function(Pointer<Void>, Int32), void Function(Pointer<Void>, int)>('library_test_TestClassEnumValueWithUnderScore_fooSentenceWithANewLineGoodCase'));
    final _handle = this.handle;
    _fooSentenceWithANewLineGoodCaseFfi(_handle, __lib.LibraryContext.isolateId);

  }

  @override
  void fooShorterSentenceWithANewLineBadCase() {
    final _fooShorterSentenceWithANewLineBadCaseFfi = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<Void Function(Pointer<Void>, Int32), void Function(Pointer<Void>, int)>('library_test_TestClassEnumValueWithUnderScore_fooShorterSentenceWithANewLineBadCase'));
    final _handle = this.handle;
    _fooShorterSentenceWithANewLineBadCaseFfi(_handle, __lib.LibraryContext.isolateId);

  }


}

Pointer<Void> testTestclassenumvaluewithunderscoreToFfi(TestClassEnumValueWithUnderScore value) =>
  _testTestclassenumvaluewithunderscoreCopyHandle((value as __lib.NativeBase).handle);

TestClassEnumValueWithUnderScore testTestclassenumvaluewithunderscoreFromFfi(Pointer<Void> handle) {
  if (handle.address == 0) throw StateError("Expected non-null value.");
  final instance = __lib.getCachedInstance(handle);
  if (instance != null && instance is TestClassEnumValueWithUnderScore) return instance;

  final _copiedHandle = _testTestclassenumvaluewithunderscoreCopyHandle(handle);
  final result = TestClassEnumValueWithUnderScore$Impl(_copiedHandle);
  __lib.cacheInstance(_copiedHandle, result);
  _testTestclassenumvaluewithunderscoreRegisterFinalizer(_copiedHandle, __lib.LibraryContext.isolateId, result);
  return result;
}

void testTestclassenumvaluewithunderscoreReleaseFfiHandle(Pointer<Void> handle) =>
  _testTestclassenumvaluewithunderscoreReleaseHandle(handle);

Pointer<Void> testTestclassenumvaluewithunderscoreToFfiNullable(TestClassEnumValueWithUnderScore? value) =>
  value != null ? testTestclassenumvaluewithunderscoreToFfi(value) : Pointer<Void>.fromAddress(0);

TestClassEnumValueWithUnderScore? testTestclassenumvaluewithunderscoreFromFfiNullable(Pointer<Void> handle) =>
  handle.address != 0 ? testTestclassenumvaluewithunderscoreFromFfi(handle) : null;

void testTestclassenumvaluewithunderscoreReleaseFfiHandleNullable(Pointer<Void> handle) =>
  _testTestclassenumvaluewithunderscoreReleaseHandle(handle);

// End of TestClassEnumValueWithUnderScore "private" section.


