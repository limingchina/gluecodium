//

//

#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#include "cbridge/include/BaseHandle.h"
#include "cbridge/include/Export.h"



_GLUECODIUM_C_EXPORT void smoke_OnlyFunctions_release_handle(_baseRef handle);
_GLUECODIUM_C_EXPORT _baseRef smoke_OnlyFunctions_copy_handle(_baseRef handle);
_GLUECODIUM_C_EXPORT const void* smoke_OnlyFunctions_get_swift_object_from_wrapper_cache(_baseRef handle);
_GLUECODIUM_C_EXPORT void smoke_OnlyFunctions_cache_swift_object_wrapper(_baseRef handle, const void* swift_pointer);
_GLUECODIUM_C_EXPORT void smoke_OnlyFunctions_remove_swift_object_from_wrapper_cache(_baseRef handle);




_GLUECODIUM_C_EXPORT _baseRef smoke_OnlyFunctions_swiftOnly(_baseRef input);

_GLUECODIUM_C_EXPORT _baseRef smoke_OnlyFunctions_shared(_baseRef input);




#ifdef __cplusplus
}
#endif
