

import 'dart:ffi';
import 'package:library/src/_library_context.dart' as __lib;
import 'package:library/src/_native_base.dart' as __lib;
import 'package:library/src/_token_cache.dart' as __lib;
import 'package:library/src/builtin_types__conversion.dart';
import 'package:meta/meta.dart';

/// Cpp is included for methods that need a native implementation.
abstract class OnlyFunctions implements Finalizable {

  static final int dartConstant = 44;


  /// - [input] String to round trip through the native implementation.
  ///
  /// Returns [String]. The unchanged input.
  ///
  static String dartOnly(String input) => $prototype.dartOnly(input);

  /// - [input] String to round trip through the native implementation.
  ///
  /// Returns [String]. The unchanged input.
  ///
  static String shared(String input) => $prototype.shared(input);

  /// @nodoc
  @visibleForTesting
  static dynamic $prototype = OnlyFunctions$Impl(Pointer<Void>.fromAddress(0));
}


// OnlyFunctions "private" section, not exported.

final _smokeOnlyfunctionsRegisterFinalizer = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Void Function(Pointer<Void>, Int32, Handle),
    void Function(Pointer<Void>, int, Object)
  >('library_smoke_OnlyFunctions_register_finalizer'));
final _smokeOnlyfunctionsCopyHandle = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_smoke_OnlyFunctions_copy_handle'));
final _smokeOnlyfunctionsReleaseHandle = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Void Function(Pointer<Void>),
    void Function(Pointer<Void>)
  >('library_smoke_OnlyFunctions_release_handle'));




/// @nodoc
@visibleForTesting

class OnlyFunctions$Impl extends __lib.NativeBase implements OnlyFunctions {

  OnlyFunctions$Impl(Pointer<Void> handle) : super(handle);

  String dartOnly(String input) {
    final _dartOnlyFfi = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<Pointer<Void> Function(Int32, Pointer<Void>), Pointer<Void> Function(int, Pointer<Void>)>('library_smoke_OnlyFunctions_dartOnly__String'));
    final _inputHandle = stringToFfi(input);
    final __resultHandle = _dartOnlyFfi(__lib.LibraryContext.isolateId, _inputHandle);
    stringReleaseFfiHandle(_inputHandle);
    try {
      return stringFromFfi(__resultHandle);
    } finally {
      stringReleaseFfiHandle(__resultHandle);

    }

  }

  String shared(String input) {
    final _sharedFfi = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<Pointer<Void> Function(Int32, Pointer<Void>), Pointer<Void> Function(int, Pointer<Void>)>('library_smoke_OnlyFunctions_shared__String'));
    final _inputHandle = stringToFfi(input);
    final __resultHandle = _sharedFfi(__lib.LibraryContext.isolateId, _inputHandle);
    stringReleaseFfiHandle(_inputHandle);
    try {
      return stringFromFfi(__resultHandle);
    } finally {
      stringReleaseFfiHandle(__resultHandle);

    }

  }


}

Pointer<Void> smokeOnlyfunctionsToFfi(OnlyFunctions value) =>
  _smokeOnlyfunctionsCopyHandle((value as __lib.NativeBase).handle);

OnlyFunctions smokeOnlyfunctionsFromFfi(Pointer<Void> handle) {
  if (handle.address == 0) throw StateError("Expected non-null value.");
  final instance = __lib.getCachedInstance(handle);
  if (instance != null && instance is OnlyFunctions) return instance;

  final _copiedHandle = _smokeOnlyfunctionsCopyHandle(handle);
  final result = OnlyFunctions$Impl(_copiedHandle);
  __lib.cacheInstance(_copiedHandle, result);
  _smokeOnlyfunctionsRegisterFinalizer(_copiedHandle, __lib.LibraryContext.isolateId, result);
  return result;
}

void smokeOnlyfunctionsReleaseFfiHandle(Pointer<Void> handle) =>
  _smokeOnlyfunctionsReleaseHandle(handle);

Pointer<Void> smokeOnlyfunctionsToFfiNullable(OnlyFunctions? value) =>
  value != null ? smokeOnlyfunctionsToFfi(value) : Pointer<Void>.fromAddress(0);

OnlyFunctions? smokeOnlyfunctionsFromFfiNullable(Pointer<Void> handle) =>
  handle.address != 0 ? smokeOnlyfunctionsFromFfi(handle) : null;

void smokeOnlyfunctionsReleaseFfiHandleNullable(Pointer<Void> handle) =>
  _smokeOnlyfunctionsReleaseHandle(handle);

// End of OnlyFunctions "private" section.
