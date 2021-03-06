import 'package:library/src/_token_cache.dart' as __lib;
import 'package:library/src/_type_repository.dart' as __lib;
import 'package:library/src/builtin_types__conversion.dart';
import 'dart:ffi';
import 'package:ffi/ffi.dart';
import 'package:meta/meta.dart';
import 'package:library/src/_library_context.dart' as __lib;
abstract class ParentClass {
  /// Destroys the underlying native object.
  ///
  /// Call this to free memory when you no longer need this instance.
  /// Note that setting the instance to null will not destroy the underlying native object.
  void release();
  rootMethod();
}
// ParentClass "private" section, not exported.
final _smoke_ParentClass_copy_handle = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_smoke_ParentClass_copy_handle'));
final _smoke_ParentClass_release_handle = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Void Function(Pointer<Void>),
    void Function(Pointer<Void>)
  >('library_smoke_ParentClass_release_handle'));
final _smoke_ParentClass_get_raw_pointer = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
      Pointer<Void> Function(Pointer<Void>),
      Pointer<Void> Function(Pointer<Void>)
    >('library_smoke_ParentClass_get_raw_pointer'));
final _smoke_ParentClass_get_type_id = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_smoke_ParentClass_get_type_id'));
class ParentClass$Impl implements ParentClass {
  @protected
  Pointer<Void> handle;
  ParentClass$Impl(this.handle);
  @override
  void release() {
    if (handle == null) return;
    __lib.reverseCache.remove(_smoke_ParentClass_get_raw_pointer(handle));
    _smoke_ParentClass_release_handle(handle);
    handle = null;
  }
  @override
  rootMethod() {
    final _rootMethod_ffi = __lib.catchArgumentError(() => __lib.nativeLibrary.lookupFunction<Void Function(Pointer<Void>, Int32), void Function(Pointer<Void>, int)>('library_smoke_ParentClass_rootMethod'));
    final _handle = this.handle;
    final __result_handle = _rootMethod_ffi(_handle, __lib.LibraryContext.isolateId);
    try {
      return (__result_handle);
    } finally {
      (__result_handle);
    }
  }
}
Pointer<Void> smoke_ParentClass_toFfi(ParentClass value) =>
  _smoke_ParentClass_copy_handle((value as ParentClass$Impl).handle);
ParentClass smoke_ParentClass_fromFfi(Pointer<Void> handle) {
  final raw_handle = _smoke_ParentClass_get_raw_pointer(handle);
  final instance = __lib.reverseCache[raw_handle] as ParentClass;
  if (instance != null) return instance;
  final _type_id_handle = _smoke_ParentClass_get_type_id(handle);
  final factoryConstructor = __lib.typeRepository[String_fromFfi(_type_id_handle)];
  String_releaseFfiHandle(_type_id_handle);
  final _copied_handle = _smoke_ParentClass_copy_handle(handle);
  final result = factoryConstructor != null
    ? factoryConstructor(_copied_handle)
    : ParentClass$Impl(_copied_handle);
  __lib.reverseCache[raw_handle] = result;
  return result;
}
void smoke_ParentClass_releaseFfiHandle(Pointer<Void> handle) =>
  _smoke_ParentClass_release_handle(handle);
Pointer<Void> smoke_ParentClass_toFfi_nullable(ParentClass value) =>
  value != null ? smoke_ParentClass_toFfi(value) : Pointer<Void>.fromAddress(0);
ParentClass smoke_ParentClass_fromFfi_nullable(Pointer<Void> handle) =>
  handle.address != 0 ? smoke_ParentClass_fromFfi(handle) : null;
void smoke_ParentClass_releaseFfiHandle_nullable(Pointer<Void> handle) =>
  _smoke_ParentClass_release_handle(handle);
// End of ParentClass "private" section.
