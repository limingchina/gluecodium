

import 'dart:ffi';
import 'package:library/src/_library_context.dart' as __lib;
import 'package:library/src/_native_base.dart' as __lib;
import 'package:library/src/_token_cache.dart' as __lib;

/// Test class for cross reference of enum values without under score.
///
/// Always working.
abstract class TestClassEnumValueWithoutUnderScore {

  /// Note:a [Error.internal] error is generated.
  ///
  void fooGoodCase();
  /// *Note: [Error.internal] error is generated.
  ///
  void fooStarGoodCase1();
  /// Note:* [Error.internal] error is generated.
  ///
  void fooStarGoodCase2();
  /// This is a test
  ///
  /// **Note:** [Error.internal] is generated.
  ///
  void fooSentenceWithANewLineGoodCase();
  /// This is a tes
  ///
  /// **Note:** [Error.internal] is generated.
  ///
  void fooShorterSentenceWithANewLineGoodCase();
}


// TestClassEnumValueWithoutUnderScore "private" section, not exported.

final _testTestclassenumvaluewithoutunderscoreRegisterFinalizer = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Void Function(Pointer<Void>, Int32, Handle),
    void Function(Pointer<Void>, int, Object)
  >('library_test_TestClassEnumValueWithoutUnderScore_register_finalizer'));
final _testTestclassenumvaluewithoutunderscoreCopyHandle = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_test_TestClassEnumValueWithoutUnderScore_copy_handle'));
final _testTestclassenumvaluewithoutunderscoreReleaseHandle = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Void Function(Pointer<Void>),
    void Function(Pointer<Void>)
  >('library_test_TestClassEnumValueWithoutUnderScore_release_handle'));







class TestClassEnumValueWithoutUnderScore$Impl extends __lib.NativeBase implements TestClassEnumValueWithoutUnderScore {

  TestClassEnumValueWithoutUnderScore$Impl(Pointer<Void> handle) : super(handle);

  @override
  void fooGoodCase() {
    final _fooGoodCaseFfi = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<Void Function(Pointer<Void>, Int32), void Function(Pointer<Void>, int)>('library_test_TestClassEnumValueWithoutUnderScore_fooGoodCase'));
    final _handle = this.handle;
    _fooGoodCaseFfi(_handle, __lib.LibraryContext.isolateId);

  }

  @override
  void fooStarGoodCase1() {
    final _fooStarGoodCase1Ffi = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<Void Function(Pointer<Void>, Int32), void Function(Pointer<Void>, int)>('library_test_TestClassEnumValueWithoutUnderScore_fooStarGoodCase1'));
    final _handle = this.handle;
    _fooStarGoodCase1Ffi(_handle, __lib.LibraryContext.isolateId);

  }

  @override
  void fooStarGoodCase2() {
    final _fooStarGoodCase2Ffi = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<Void Function(Pointer<Void>, Int32), void Function(Pointer<Void>, int)>('library_test_TestClassEnumValueWithoutUnderScore_fooStarGoodCase2'));
    final _handle = this.handle;
    _fooStarGoodCase2Ffi(_handle, __lib.LibraryContext.isolateId);

  }

  @override
  void fooSentenceWithANewLineGoodCase() {
    final _fooSentenceWithANewLineGoodCaseFfi = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<Void Function(Pointer<Void>, Int32), void Function(Pointer<Void>, int)>('library_test_TestClassEnumValueWithoutUnderScore_fooSentenceWithANewLineGoodCase'));
    final _handle = this.handle;
    _fooSentenceWithANewLineGoodCaseFfi(_handle, __lib.LibraryContext.isolateId);

  }

  @override
  void fooShorterSentenceWithANewLineGoodCase() {
    final _fooShorterSentenceWithANewLineGoodCaseFfi = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<Void Function(Pointer<Void>, Int32), void Function(Pointer<Void>, int)>('library_test_TestClassEnumValueWithoutUnderScore_fooShorterSentenceWithANewLineGoodCase'));
    final _handle = this.handle;
    _fooShorterSentenceWithANewLineGoodCaseFfi(_handle, __lib.LibraryContext.isolateId);

  }


}

Pointer<Void> testTestclassenumvaluewithoutunderscoreToFfi(TestClassEnumValueWithoutUnderScore value) =>
  _testTestclassenumvaluewithoutunderscoreCopyHandle((value as __lib.NativeBase).handle);

TestClassEnumValueWithoutUnderScore testTestclassenumvaluewithoutunderscoreFromFfi(Pointer<Void> handle) {
  if (handle.address == 0) throw StateError("Expected non-null value.");
  final instance = __lib.getCachedInstance(handle);
  if (instance != null && instance is TestClassEnumValueWithoutUnderScore) return instance;

  final _copiedHandle = _testTestclassenumvaluewithoutunderscoreCopyHandle(handle);
  final result = TestClassEnumValueWithoutUnderScore$Impl(_copiedHandle);
  __lib.cacheInstance(_copiedHandle, result);
  _testTestclassenumvaluewithoutunderscoreRegisterFinalizer(_copiedHandle, __lib.LibraryContext.isolateId, result);
  return result;
}

void testTestclassenumvaluewithoutunderscoreReleaseFfiHandle(Pointer<Void> handle) =>
  _testTestclassenumvaluewithoutunderscoreReleaseHandle(handle);

Pointer<Void> testTestclassenumvaluewithoutunderscoreToFfiNullable(TestClassEnumValueWithoutUnderScore? value) =>
  value != null ? testTestclassenumvaluewithoutunderscoreToFfi(value) : Pointer<Void>.fromAddress(0);

TestClassEnumValueWithoutUnderScore? testTestclassenumvaluewithoutunderscoreFromFfiNullable(Pointer<Void> handle) =>
  handle.address != 0 ? testTestclassenumvaluewithoutunderscoreFromFfi(handle) : null;

void testTestclassenumvaluewithoutunderscoreReleaseFfiHandleNullable(Pointer<Void> handle) =>
  _testTestclassenumvaluewithoutunderscoreReleaseHandle(handle);

// End of TestClassEnumValueWithoutUnderScore "private" section.


