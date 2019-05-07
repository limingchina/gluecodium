//
//
// Automatically generated. Do not modify. Your changes will be lost.
#include "cbridge/include/smoke/cbridge_StructsWithMethodsInterface.h"
#include "cbridge_internal/include/BaseHandleImpl.h"
#include "genium/Optional.h"
#include "smoke/StructsWithMethodsInterface.h"
#include <memory>
#include <new>
void smoke_StructsWithMethodsInterface_release_handle(_baseRef handle) {
    delete get_pointer<std::shared_ptr<::smoke::StructsWithMethodsInterface>>(handle);
}
_baseRef smoke_StructsWithMethodsInterface_copy_handle(_baseRef handle) {
    return handle
        ? reinterpret_cast<_baseRef>(checked_pointer_copy(*get_pointer<std::shared_ptr<::smoke::StructsWithMethodsInterface>>(handle)))
        : 0;
}
_baseRef
smoke_StructsWithMethodsInterface_Vector3_create_handle( double x, double y, double z )
{
    ::smoke::StructsWithMethodsInterface::Vector3* _struct = new ( std::nothrow ) ::smoke::StructsWithMethodsInterface::Vector3();
    _struct->x = x;
    _struct->y = y;
    _struct->z = z;
    return reinterpret_cast<_baseRef>( _struct );
}
void
smoke_StructsWithMethodsInterface_Vector3_release_handle( _baseRef handle )
{
    delete get_pointer<::smoke::StructsWithMethodsInterface::Vector3>( handle );
}
_baseRef
smoke_StructsWithMethodsInterface_Vector3_create_optional_handle(double x, double y, double z)
{
    auto _struct = new ( std::nothrow ) ::genium::optional<::smoke::StructsWithMethodsInterface::Vector3>( ::smoke::StructsWithMethodsInterface::Vector3( ) );
    (*_struct)->x = x;
    (*_struct)->y = y;
    (*_struct)->z = z;
    return reinterpret_cast<_baseRef>( _struct );
}
_baseRef
smoke_StructsWithMethodsInterface_Vector3_unwrap_optional_handle( _baseRef handle )
{
    return reinterpret_cast<_baseRef>( &**reinterpret_cast<::genium::optional<::smoke::StructsWithMethodsInterface::Vector3>*>( handle ) );
}
void smoke_StructsWithMethodsInterface_Vector3_release_optional_handle(_baseRef handle) {
    delete reinterpret_cast<::genium::optional<::smoke::StructsWithMethodsInterface::Vector3>*>( handle );
}
double smoke_StructsWithMethodsInterface_Vector3_x_get(_baseRef handle) {
    auto struct_pointer = get_pointer<::smoke::StructsWithMethodsInterface::Vector3>(handle);
return struct_pointer->x;
}
double smoke_StructsWithMethodsInterface_Vector3_y_get(_baseRef handle) {
    auto struct_pointer = get_pointer<::smoke::StructsWithMethodsInterface::Vector3>(handle);
return struct_pointer->y;
}
double smoke_StructsWithMethodsInterface_Vector3_z_get(_baseRef handle) {
    auto struct_pointer = get_pointer<::smoke::StructsWithMethodsInterface::Vector3>(handle);
return struct_pointer->z;
}
double smoke_StructsWithMethodsInterface_Vector3_distanceTo(_baseRef _instance, _baseRef other) {
    return get_pointer<::smoke::StructsWithMethodsInterface::Vector3>(_instance)->distance_to(Conversion<::smoke::StructsWithMethodsInterface::Vector3>::toCpp(other))
;
}
_baseRef smoke_StructsWithMethodsInterface_Vector3_add(_baseRef _instance, _baseRef other) {
    return Conversion<::smoke::StructsWithMethodsInterface::Vector3>::toBaseRef(get_pointer<::smoke::StructsWithMethodsInterface::Vector3>(_instance)->add(Conversion<::smoke::StructsWithMethodsInterface::Vector3>::toCpp(other)))
;
}
