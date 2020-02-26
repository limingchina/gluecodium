#include "ffi_smoke_CalculatorListener.h"
#include "ConversionBase.h"
#include "gluecodium/VectorHash.h"
#include "smoke/CalculationResult.h"
#include "smoke/CalculatorListener.h"
#include <memory>
#include <vector>
#include <memory>
#include <new>
class smoke_CalculatorListener_Proxy : public ::smoke::CalculatorListener {
public:
    smoke_CalculatorListener_Proxy(uint64_t token, FfiOpaqueHandle f0, FfiOpaqueHandle f1, FfiOpaqueHandle f2, FfiOpaqueHandle f3, FfiOpaqueHandle f4, FfiOpaqueHandle f5)
        : token(token), f0(f0), f1(f1), f2(f2), f3(f3), f4(f4), f5(f5) { }
    void
    on_calculation_result(const double calculationResult) override {
        int64_t _error = (*reinterpret_cast<int64_t (*)(uint64_t, double)>(f0))(token,
            gluecodium::ffi::Conversion<double>::toFfi(calculationResult)
        );
    }
    void
    on_calculation_result_const(const double calculationResult) const override {
        int64_t _error = (*reinterpret_cast<int64_t (*)(uint64_t, double)>(f1))(token,
            gluecodium::ffi::Conversion<double>::toFfi(calculationResult)
        );
    }
    void
    on_calculation_result_struct(const ::smoke::CalculatorListener::ResultStruct& calculationResult) override {
        int64_t _error = (*reinterpret_cast<int64_t (*)(uint64_t, FfiOpaqueHandle)>(f2))(token,
            gluecodium::ffi::Conversion<::smoke::CalculatorListener::ResultStruct>::toFfi(calculationResult)
        );
    }
    void
    on_calculation_result_array(const std::vector<double>& calculationResult) override {
        int64_t _error = (*reinterpret_cast<int64_t (*)(uint64_t, FfiOpaqueHandle)>(f3))(token,
            gluecodium::ffi::Conversion<std::vector<double>>::toFfi(calculationResult)
        );
    }
    void
    on_calculation_result_map(const std::unordered_map<std::string, double>& calculationResults) override {
        int64_t _error = (*reinterpret_cast<int64_t (*)(uint64_t, FfiOpaqueHandle)>(f4))(token,
            gluecodium::ffi::Conversion<std::unordered_map<std::string, double>>::toFfi(calculationResults)
        );
    }
    void
    on_calculation_result_instance(const std::shared_ptr<::smoke::CalculationResult>& calculationResult) override {
        int64_t _error = (*reinterpret_cast<int64_t (*)(uint64_t, FfiOpaqueHandle)>(f5))(token,
            gluecodium::ffi::Conversion<std::shared_ptr<::smoke::CalculationResult>>::toFfi(calculationResult)
        );
    }
private:
    uint64_t token;
    FfiOpaqueHandle f0;
    FfiOpaqueHandle f1;
    FfiOpaqueHandle f2;
    FfiOpaqueHandle f3;
    FfiOpaqueHandle f4;
    FfiOpaqueHandle f5;
};
#ifdef __cplusplus
extern "C" {
#endif
void
smoke_CalculatorListener_onCalculationResult__Double(FfiOpaqueHandle _self, double calculationResult) {
            (*gluecodium::ffi::Conversion<std::shared_ptr<::smoke::CalculatorListener>>::toCpp(_self)).on_calculation_result(
            gluecodium::ffi::Conversion<double>::toCpp(calculationResult)
        );
}
void
smoke_CalculatorListener_onCalculationResultConst__Double(FfiOpaqueHandle _self, double calculationResult) {
            (*gluecodium::ffi::Conversion<std::shared_ptr<::smoke::CalculatorListener>>::toCpp(_self)).on_calculation_result_const(
            gluecodium::ffi::Conversion<double>::toCpp(calculationResult)
        );
}
void
smoke_CalculatorListener_onCalculationResultStruct__ResultStruct(FfiOpaqueHandle _self, FfiOpaqueHandle calculationResult) {
            (*gluecodium::ffi::Conversion<std::shared_ptr<::smoke::CalculatorListener>>::toCpp(_self)).on_calculation_result_struct(
            gluecodium::ffi::Conversion<::smoke::CalculatorListener::ResultStruct>::toCpp(calculationResult)
        );
}
void
smoke_CalculatorListener_onCalculationResultArray__ListOf_1Double(FfiOpaqueHandle _self, FfiOpaqueHandle calculationResult) {
            (*gluecodium::ffi::Conversion<std::shared_ptr<::smoke::CalculatorListener>>::toCpp(_self)).on_calculation_result_array(
            gluecodium::ffi::Conversion<std::vector<double>>::toCpp(calculationResult)
        );
}
void
smoke_CalculatorListener_onCalculationResultMap__MapOf_1String_1to_1Double(FfiOpaqueHandle _self, FfiOpaqueHandle calculationResults) {
            (*gluecodium::ffi::Conversion<std::shared_ptr<::smoke::CalculatorListener>>::toCpp(_self)).on_calculation_result_map(
            gluecodium::ffi::Conversion<std::unordered_map<std::string, double>>::toCpp(calculationResults)
        );
}
void
smoke_CalculatorListener_onCalculationResultInstance__CalculationResult(FfiOpaqueHandle _self, FfiOpaqueHandle calculationResult) {
            (*gluecodium::ffi::Conversion<std::shared_ptr<::smoke::CalculatorListener>>::toCpp(_self)).on_calculation_result_instance(
            gluecodium::ffi::Conversion<std::shared_ptr<::smoke::CalculationResult>>::toCpp(calculationResult)
        );
}
FfiOpaqueHandle
smoke_CalculatorListener_copy_handle(FfiOpaqueHandle handle) {
    return reinterpret_cast<FfiOpaqueHandle>(
        new (std::nothrow) std::shared_ptr<::smoke::CalculatorListener>(
            *reinterpret_cast<std::shared_ptr<::smoke::CalculatorListener>*>(handle)
        )
    );
}
void
smoke_CalculatorListener_release_handle(FfiOpaqueHandle handle) {
    delete reinterpret_cast<std::shared_ptr<::smoke::CalculatorListener>*>(handle);
}
FfiOpaqueHandle
smoke_CalculatorListener_create_proxy(uint64_t token, FfiOpaqueHandle f0, FfiOpaqueHandle f1, FfiOpaqueHandle f2, FfiOpaqueHandle f3, FfiOpaqueHandle f4, FfiOpaqueHandle f5) {
    return reinterpret_cast<FfiOpaqueHandle>(
        new (std::nothrow) std::shared_ptr<::smoke::CalculatorListener>(
            new (std::nothrow) smoke_CalculatorListener_Proxy(token, f0, f1, f2, f3, f4, f5)
        )
    );
}
FfiOpaqueHandle
smoke_CalculatorListener_get_raw_pointer(FfiOpaqueHandle handle) {
    return reinterpret_cast<FfiOpaqueHandle>(
        reinterpret_cast<std::shared_ptr<::smoke::CalculatorListener>*>(handle)->get()
    );
}
FfiOpaqueHandle
smoke_CalculatorListener_ResultStruct_create_handle(double result) {
    auto _result = new (std::nothrow) ::smoke::CalculatorListener::ResultStruct(gluecodium::ffi::Conversion<double>::toCpp(result));
    return reinterpret_cast<FfiOpaqueHandle>(_result);
}
void
smoke_CalculatorListener_ResultStruct_release_handle(FfiOpaqueHandle handle) {
    delete reinterpret_cast<::smoke::CalculatorListener::ResultStruct*>(handle);
}
double
smoke_CalculatorListener_ResultStruct_get_field_result(FfiOpaqueHandle handle) {
    return gluecodium::ffi::Conversion<double>::toFfi(
        reinterpret_cast<::smoke::CalculatorListener::ResultStruct*>(handle)->result
    );
}
FfiOpaqueHandle
smoke_CalculatorListener_ResultStruct_create_handle_nullable(FfiOpaqueHandle value)
{
    return reinterpret_cast<FfiOpaqueHandle>(
        new (std::nothrow) gluecodium::optional<::smoke::CalculatorListener::ResultStruct>(
            gluecodium::ffi::Conversion<::smoke::CalculatorListener::ResultStruct>::toCpp(value)
        )
    );
}
void
smoke_CalculatorListener_ResultStruct_release_handle_nullable(FfiOpaqueHandle handle)
{
    delete reinterpret_cast<gluecodium::optional<::smoke::CalculatorListener::ResultStruct>*>(handle);
}
FfiOpaqueHandle
smoke_CalculatorListener_ResultStruct_get_value_nullable(FfiOpaqueHandle handle)
{
    return gluecodium::ffi::Conversion<::smoke::CalculatorListener::ResultStruct>::toFfi(
        **reinterpret_cast<gluecodium::optional<::smoke::CalculatorListener::ResultStruct>*>(handle)
    );
}
#ifdef __cplusplus
}
#endif