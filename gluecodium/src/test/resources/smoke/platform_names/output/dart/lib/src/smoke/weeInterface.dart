import 'package:library/src/BuiltInTypes__conversion.dart';
import 'package:library/src/smoke/weeTypes.dart';
import 'dart:ffi';
import 'package:ffi/ffi.dart';
import 'package:meta/meta.dart';
import 'package:library/src/_library_init.dart' as __lib;
final _smoke_PlatformNamesInterface_copy_handle = __lib.nativeLibrary.lookupFunction<
    Pointer<Void> Function(Pointer<Void>),
    Pointer<Void> Function(Pointer<Void>)
  >('library_smoke_PlatformNamesInterface_copy_handle');
final _smoke_PlatformNamesInterface_release_handle = __lib.nativeLibrary.lookupFunction<
    Void Function(Pointer<Void>),
    void Function(Pointer<Void>)
  >('library_smoke_PlatformNamesInterface_release_handle');
class weeInterface {
  final Pointer<Void> _handle;
  weeInterface._(this._handle);
  void release() => _smoke_PlatformNamesInterface_release_handle(_handle);
  weeInterface(String makeParameter) : this._(_make(makeParameter));
  weeStruct WeeMethod(String WeeParameter) {
    final _WeeMethod_ffi = __lib.nativeLibrary.lookupFunction<Pointer<Void> Function(Pointer<Void>, Pointer<Void>), Pointer<Void> Function(Pointer<Void>, Pointer<Void>)>('library_smoke_PlatformNamesInterface_basicMethod__String');
    final _WeeParameter_handle = String_toFfi(WeeParameter);
    final __result_handle = _WeeMethod_ffi(_handle, _WeeParameter_handle);
    String_releaseFfiHandle(_WeeParameter_handle);
    final _result = smoke_PlatformNames_BasicStruct_fromFfi(__result_handle);
    smoke_PlatformNames_BasicStruct_releaseFfiHandle(__result_handle);
    return _result;
  }
  static Pointer<Void> _make(String makeParameter) {
    final _make_ffi = __lib.nativeLibrary.lookupFunction<Pointer<Void> Function(Pointer<Void>), Pointer<Void> Function(Pointer<Void>)>('library_smoke_PlatformNamesInterface_create__String');
    final _makeParameter_handle = String_toFfi(makeParameter);
    final __result_handle = _make_ffi(_makeParameter_handle);
    String_releaseFfiHandle(_makeParameter_handle);
    return __result_handle;
  }
  int get WEE_PROPERTY {
    final _get_ffi = __lib.nativeLibrary.lookupFunction<Uint32 Function(Pointer<Void>), int Function(Pointer<Void>)>('library_smoke_PlatformNamesInterface_basicProperty_get');
    final __result_handle = _get_ffi(_handle);
    final _result = (__result_handle);
    (__result_handle);
    return _result;
  }
  set WEE_PROPERTY(int value) {
    final _set_ffi = __lib.nativeLibrary.lookupFunction<Void Function(Pointer<Void>, Uint32), void Function(Pointer<Void>, int)>('library_smoke_PlatformNamesInterface_basicProperty_set__UInt');
    final _value_handle = (value);
    final __result_handle = _set_ffi(_handle, _value_handle);
    (_value_handle);
    final _result = (__result_handle);
    (__result_handle);
    return _result;
  }
}
Pointer<Void> smoke_PlatformNamesInterface_toFfi(weeInterface value) =>
  _smoke_PlatformNamesInterface_copy_handle(value._handle);
weeInterface smoke_PlatformNamesInterface_fromFfi(Pointer<Void> handle) =>
  weeInterface._(_smoke_PlatformNamesInterface_copy_handle(handle));
void smoke_PlatformNamesInterface_releaseFfiHandle(Pointer<Void> handle) =>
  _smoke_PlatformNamesInterface_release_handle(handle);
Pointer<Void> smoke_PlatformNamesInterface_toFfi_nullable(weeInterface value) =>
  value != null ? smoke_PlatformNamesInterface_toFfi(value) : Pointer<Void>.fromAddress(0);
weeInterface smoke_PlatformNamesInterface_fromFfi_nullable(Pointer<Void> handle) =>
  handle.address != 0 ? smoke_PlatformNamesInterface_fromFfi(handle) : null;
void smoke_PlatformNamesInterface_releaseFfiHandle_nullable(Pointer<Void> handle) =>
  _smoke_PlatformNamesInterface_release_handle(handle);
