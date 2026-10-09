
#include "ffi_smoke_OnlyFunctions.h"

#include "ConversionBase.h"
#include "InstanceCache.h"
#include "FinalizerData.h"
#include "IsolateContext.h"
#include "smoke/OnlyFunctions.h"
#include <memory>
#include <string>
#include <memory>
#include <new>


#ifdef __cplusplus
extern "C" {
#endif




FfiOpaqueHandle
library_smoke_OnlyFunctions_dartOnly__String(int32_t _isolate_id, FfiOpaqueHandle input) {
    gluecodium::ffi::IsolateContext _isolate_context(_isolate_id);
    return gluecodium::ffi::Conversion<std::string>::toFfi(
        smoke::OnlyFunctions::dart_only(
            gluecodium::ffi::Conversion<std::string>::toCpp(input)
        )
    );
}



FfiOpaqueHandle
library_smoke_OnlyFunctions_shared__String(int32_t _isolate_id, FfiOpaqueHandle input) {
    gluecodium::ffi::IsolateContext _isolate_context(_isolate_id);
    return gluecodium::ffi::Conversion<std::string>::toFfi(
        smoke::OnlyFunctions::shared(
            gluecodium::ffi::Conversion<std::string>::toCpp(input)
        )
    );
}















// "Private" finalizer, not exposed to be callable from Dart.
void
library_smoke_OnlyFunctions_finalizer(FfiOpaqueHandle handle, int32_t isolate_id) {
    auto ptr_ptr = reinterpret_cast<std::shared_ptr<smoke::OnlyFunctions>*>(handle);
    library_uncache_dart_handle_by_raw_pointer(ptr_ptr->get(), isolate_id);
    library_smoke_OnlyFunctions_release_handle(handle);
}

void
library_smoke_OnlyFunctions_register_finalizer(FfiOpaqueHandle ffi_handle, int32_t isolate_id, Dart_Handle dart_handle) {
    FinalizerData* data = new (std::nothrow) FinalizerData{ffi_handle, isolate_id, &library_smoke_OnlyFunctions_finalizer};
    Dart_NewFinalizableHandle_DL(dart_handle, data, sizeof data, &library_execute_finalizer);
}

FfiOpaqueHandle
library_smoke_OnlyFunctions_copy_handle(FfiOpaqueHandle handle) {
    return reinterpret_cast<FfiOpaqueHandle>(
        new (std::nothrow) std::shared_ptr<smoke::OnlyFunctions>(
            *reinterpret_cast<std::shared_ptr<smoke::OnlyFunctions>*>(handle)
        )
    );
}

void
library_smoke_OnlyFunctions_release_handle(FfiOpaqueHandle handle) {
    delete reinterpret_cast<std::shared_ptr<smoke::OnlyFunctions>*>(handle);
}







#ifdef __cplusplus
}
#endif
