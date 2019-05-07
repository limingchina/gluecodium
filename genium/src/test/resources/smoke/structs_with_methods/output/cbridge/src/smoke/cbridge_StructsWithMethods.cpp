//
//
// Automatically generated. Do not modify. Your changes will be lost.
#include "cbridge/include/smoke/cbridge_StructsWithMethods.h"
#include "cbridge_internal/include/BaseHandleImpl.h"
#include "genium/Optional.h"
#include "smoke/StructsWithMethods.h"
#include <memory>
#include <new>
_baseRef
smoke_StructsWithMethods_Vector_create_handle( double x, double y )
{
    ::smoke::Vector* _struct = new ( std::nothrow ) ::smoke::Vector();
    _struct->x = x;
    _struct->y = y;
    return reinterpret_cast<_baseRef>( _struct );
}
void
smoke_StructsWithMethods_Vector_release_handle( _baseRef handle )
{
    delete get_pointer<::smoke::Vector>( handle );
}
_baseRef
smoke_StructsWithMethods_Vector_create_optional_handle(double x, double y)
{
    auto _struct = new ( std::nothrow ) ::genium::optional<::smoke::Vector>( ::smoke::Vector( ) );
    (*_struct)->x = x;
    (*_struct)->y = y;
    return reinterpret_cast<_baseRef>( _struct );
}
_baseRef
smoke_StructsWithMethods_Vector_unwrap_optional_handle( _baseRef handle )
{
    return reinterpret_cast<_baseRef>( &**reinterpret_cast<::genium::optional<::smoke::Vector>*>( handle ) );
}
void smoke_StructsWithMethods_Vector_release_optional_handle(_baseRef handle) {
    delete reinterpret_cast<::genium::optional<::smoke::Vector>*>( handle );
}
double smoke_StructsWithMethods_Vector_x_get(_baseRef handle) {
    auto struct_pointer = get_pointer<::smoke::Vector>(handle);
return struct_pointer->x;
}
double smoke_StructsWithMethods_Vector_y_get(_baseRef handle) {
    auto struct_pointer = get_pointer<::smoke::Vector>(handle);
return struct_pointer->y;
}
double smoke_StructsWithMethods_Vector_distanceTo(_baseRef _instance, _baseRef other) {
    return get_pointer<::smoke::Vector>(_instance)->distance_to(Conversion<::smoke::Vector>::toCpp(other))
;
}
_baseRef smoke_StructsWithMethods_Vector_add(_baseRef _instance, _baseRef other) {
    return Conversion<::smoke::Vector>::toBaseRef(get_pointer<::smoke::Vector>(_instance)->add(Conversion<::smoke::Vector>::toCpp(other)))
;
}
