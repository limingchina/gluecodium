import 'package:library/src/_token_cache.dart' as __lib;
import 'package:library/src/_type_repository.dart' as __lib;
import 'package:library/src/builtin_types__conversion.dart';
import 'package:library/src/smoke/public_class.dart';
import 'dart:ffi';
import 'package:ffi/ffi.dart';
import 'package:meta/meta.dart';
import 'package:library/src/_library_context.dart' as __lib;
abstract class PublicInterface {
  /// Destroys the underlying native object.
  ///
  /// Call this to free memory when you no longer need this instance.
  /// Note that setting the instance to null will not destroy the underlying native object.
  void release() {}
}
/// @nodoc
class PublicInterface_InternalStruct {
  /// @nodoc
  PublicClass_InternalStruct internal_fieldOfInternalType;
  PublicInterface_InternalStruct(this.internal_fieldOfInternalType);
}
// PublicInterface_InternalStruct "private" section, not exported.
final _smoke_PublicInterface_InternalStruct_create_handle = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_smoke_PublicInterface_InternalStruct_create_handle'));
final _smoke_PublicInterface_InternalStruct_release_handle = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Void Function(Pointer<Void>),
    void Function(Pointer<Void>)
  >('library_smoke_PublicInterface_InternalStruct_release_handle'));
final _smoke_PublicInterface_InternalStruct_get_field_fieldOfInternalType = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_smoke_PublicInterface_InternalStruct_get_field_fieldOfInternalType'));
Pointer<Void> smoke_PublicInterface_InternalStruct_toFfi(PublicInterface_InternalStruct value) {
  final _fieldOfInternalType_handle = smoke_PublicClass_InternalStruct_toFfi(value.internal_fieldOfInternalType);
  final _result = _smoke_PublicInterface_InternalStruct_create_handle(_fieldOfInternalType_handle);
  smoke_PublicClass_InternalStruct_releaseFfiHandle(_fieldOfInternalType_handle);
  return _result;
}
PublicInterface_InternalStruct smoke_PublicInterface_InternalStruct_fromFfi(Pointer<Void> handle) {
  final _fieldOfInternalType_handle = _smoke_PublicInterface_InternalStruct_get_field_fieldOfInternalType(handle);
  try {
    return PublicInterface_InternalStruct(
      smoke_PublicClass_InternalStruct_fromFfi(_fieldOfInternalType_handle)
    );
  } finally {
    smoke_PublicClass_InternalStruct_releaseFfiHandle(_fieldOfInternalType_handle);
  }
}
void smoke_PublicInterface_InternalStruct_releaseFfiHandle(Pointer<Void> handle) => _smoke_PublicInterface_InternalStruct_release_handle(handle);
// Nullable PublicInterface_InternalStruct
final _smoke_PublicInterface_InternalStruct_create_handle_nullable = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_smoke_PublicInterface_InternalStruct_create_handle_nullable'));
final _smoke_PublicInterface_InternalStruct_release_handle_nullable = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Void Function(Pointer<Void>),
    void Function(Pointer<Void>)
  >('library_smoke_PublicInterface_InternalStruct_release_handle_nullable'));
final _smoke_PublicInterface_InternalStruct_get_value_nullable = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_smoke_PublicInterface_InternalStruct_get_value_nullable'));
Pointer<Void> smoke_PublicInterface_InternalStruct_toFfi_nullable(PublicInterface_InternalStruct value) {
  if (value == null) return Pointer<Void>.fromAddress(0);
  final _handle = smoke_PublicInterface_InternalStruct_toFfi(value);
  final result = _smoke_PublicInterface_InternalStruct_create_handle_nullable(_handle);
  smoke_PublicInterface_InternalStruct_releaseFfiHandle(_handle);
  return result;
}
PublicInterface_InternalStruct smoke_PublicInterface_InternalStruct_fromFfi_nullable(Pointer<Void> handle) {
  if (handle.address == 0) return null;
  final _handle = _smoke_PublicInterface_InternalStruct_get_value_nullable(handle);
  final result = smoke_PublicInterface_InternalStruct_fromFfi(_handle);
  smoke_PublicInterface_InternalStruct_releaseFfiHandle(_handle);
  return result;
}
void smoke_PublicInterface_InternalStruct_releaseFfiHandle_nullable(Pointer<Void> handle) =>
  _smoke_PublicInterface_InternalStruct_release_handle_nullable(handle);
// End of PublicInterface_InternalStruct "private" section.
// PublicInterface "private" section, not exported.
final _smoke_PublicInterface_copy_handle = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_smoke_PublicInterface_copy_handle'));
final _smoke_PublicInterface_release_handle = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Void Function(Pointer<Void>),
    void Function(Pointer<Void>)
  >('library_smoke_PublicInterface_release_handle'));
final _smoke_PublicInterface_create_proxy = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Uint64, Int32, Pointer),
    Pointer<Void> Function(int, int, Pointer)
  >('library_smoke_PublicInterface_create_proxy'));
final _smoke_PublicInterface_get_raw_pointer = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
      Pointer<Void> Function(Pointer<Void>),
      Pointer<Void> Function(Pointer<Void>)
    >('library_smoke_PublicInterface_get_raw_pointer'));
final _smoke_PublicInterface_get_type_id = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_smoke_PublicInterface_get_type_id'));
class PublicInterface$Impl implements PublicInterface {
  @protected
  Pointer<Void> handle;
  PublicInterface$Impl(this.handle);
  @override
  void release() {
    if (handle == null) return;
    __lib.reverseCache.remove(_smoke_PublicInterface_get_raw_pointer(handle));
    _smoke_PublicInterface_release_handle(handle);
    handle = null;
  }
}
Pointer<Void> smoke_PublicInterface_toFfi(PublicInterface value) {
  if (value is PublicInterface$Impl) return _smoke_PublicInterface_copy_handle(value.handle);
  final result = _smoke_PublicInterface_create_proxy(
    __lib.cacheObject(value),
    __lib.LibraryContext.isolateId,
    __lib.uncacheObjectFfi
  );
  __lib.reverseCache[_smoke_PublicInterface_get_raw_pointer(result)] = value;
  return result;
}
PublicInterface smoke_PublicInterface_fromFfi(Pointer<Void> handle) {
  final raw_handle = _smoke_PublicInterface_get_raw_pointer(handle);
  final instance = __lib.reverseCache[raw_handle] as PublicInterface;
  if (instance != null) return instance;
  final _type_id_handle = _smoke_PublicInterface_get_type_id(handle);
  final factoryConstructor = __lib.typeRepository[String_fromFfi(_type_id_handle)];
  String_releaseFfiHandle(_type_id_handle);
  final _copied_handle = _smoke_PublicInterface_copy_handle(handle);
  final result = factoryConstructor != null
    ? factoryConstructor(_copied_handle)
    : PublicInterface$Impl(_copied_handle);
  __lib.reverseCache[raw_handle] = result;
  return result;
}
void smoke_PublicInterface_releaseFfiHandle(Pointer<Void> handle) =>
  _smoke_PublicInterface_release_handle(handle);
Pointer<Void> smoke_PublicInterface_toFfi_nullable(PublicInterface value) =>
  value != null ? smoke_PublicInterface_toFfi(value) : Pointer<Void>.fromAddress(0);
PublicInterface smoke_PublicInterface_fromFfi_nullable(Pointer<Void> handle) =>
  handle.address != 0 ? smoke_PublicInterface_fromFfi(handle) : null;
void smoke_PublicInterface_releaseFfiHandle_nullable(Pointer<Void> handle) =>
  _smoke_PublicInterface_release_handle(handle);
// End of PublicInterface "private" section.
