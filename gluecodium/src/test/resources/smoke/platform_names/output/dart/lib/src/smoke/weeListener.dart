import 'package:library/src/BuiltInTypes__conversion.dart';
import 'package:library/src/_token_cache.dart' as __lib;
import 'package:library/src/_type_repository.dart' as __lib;
import 'dart:ffi';
import 'package:ffi/ffi.dart';
import 'package:meta/meta.dart';
import 'package:library/src/_library_context.dart' as __lib;

abstract class weeListener {
  void release() {}
  WeeMethod(String WeeParameter);
}
// weeListener "private" section, not exported.
final _smoke_PlatformNamesListener_copy_handle = __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_smoke_PlatformNamesListener_copy_handle');
final _smoke_PlatformNamesListener_release_handle = __lib.nativeLibrary.lookupFunction<
    Void Function(Pointer<Void>),
    void Function(Pointer<Void>)
  >('library_smoke_PlatformNamesListener_release_handle');
final _smoke_PlatformNamesListener_create_proxy = __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Uint64, Int32, Pointer, Pointer),
    Pointer<Void> Function(int, int, Pointer, Pointer)
  >('library_smoke_PlatformNamesListener_create_proxy');
final _smoke_PlatformNamesListener_get_raw_pointer = __lib.nativeLibrary.lookupFunction<
      Pointer<Void> Function(Pointer<Void>),
      Pointer<Void> Function(Pointer<Void>)
    >('library_smoke_PlatformNamesListener_get_raw_pointer');
final _smoke_PlatformNamesListener_get_type_id = __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_smoke_PlatformNamesListener_get_type_id');
class weeListener$Impl implements weeListener {
  final Pointer<Void> handle;
  weeListener$Impl(this.handle);
  @override
  void release() => _smoke_PlatformNamesListener_release_handle(handle);
  @override
  WeeMethod(String WeeParameter) {
    final _WeeMethod_ffi = __lib.nativeLibrary.lookupFunction<Void Function(Pointer<Void>, Int32, Pointer<Void>), void Function(Pointer<Void>, int, Pointer<Void>)>('library_smoke_PlatformNamesListener_basicMethod__String');
    final _WeeParameter_handle = String_toFfi(WeeParameter);
    final _handle = this.handle;
    final __result_handle = _WeeMethod_ffi(_handle, __lib.LibraryContext.isolateId, _WeeParameter_handle);
    String_releaseFfiHandle(_WeeParameter_handle);
    final _result = (__result_handle);
    (__result_handle);
    return _result;
  }
}
int _weeListener_WeeMethod_static(int _token, Pointer<Void> WeeParameter) {
  final __WeeParameter = String_fromFfi(WeeParameter);
  String_releaseFfiHandle(WeeParameter);
  (__lib.instanceCache[_token] as weeListener).WeeMethod(__WeeParameter);
  return 0;
}
Pointer<Void> smoke_PlatformNamesListener_toFfi(weeListener value) {
  if (value is weeListener$Impl) return _smoke_PlatformNamesListener_copy_handle(value.handle);
  final result = _smoke_PlatformNamesListener_create_proxy(
    __lib.cacheObject(value),
    __lib.LibraryContext.isolateId,
    __lib.uncacheObjectFfi,
    Pointer.fromFunction<Int64 Function(Uint64, Pointer<Void>)>(_weeListener_WeeMethod_static, __lib.unknownError)
  );
  __lib.reverseCache[_smoke_PlatformNamesListener_get_raw_pointer(result)] = value;
  return result;
}
weeListener smoke_PlatformNamesListener_fromFfi(Pointer<Void> handle) {
  final instance = __lib.reverseCache[_smoke_PlatformNamesListener_get_raw_pointer(handle)] as weeListener;
  if (instance != null) return instance;
  final _copied_handle = _smoke_PlatformNamesListener_copy_handle(handle);
  final _type_id_handle = _smoke_PlatformNamesListener_get_type_id(handle);
  final factoryConstructor = __lib.typeRepository[String_fromFfi(_type_id_handle)];
  final result = factoryConstructor == null
    ? weeListener$Impl(_copied_handle)
    : factoryConstructor(_copied_handle);
  String_releaseFfiHandle(_type_id_handle);
  return result;
}
void smoke_PlatformNamesListener_releaseFfiHandle(Pointer<Void> handle) =>
  _smoke_PlatformNamesListener_release_handle(handle);
Pointer<Void> smoke_PlatformNamesListener_toFfi_nullable(weeListener value) =>
  value != null ? smoke_PlatformNamesListener_toFfi(value) : Pointer<Void>.fromAddress(0);
weeListener smoke_PlatformNamesListener_fromFfi_nullable(Pointer<Void> handle) =>
  handle.address != 0 ? smoke_PlatformNamesListener_fromFfi(handle) : null;
void smoke_PlatformNamesListener_releaseFfiHandle_nullable(Pointer<Void> handle) =>
  _smoke_PlatformNamesListener_release_handle(handle);
// End of weeListener "private" section.
