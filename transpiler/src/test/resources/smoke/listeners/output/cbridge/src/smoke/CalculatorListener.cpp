//
// Copyright (C) 2017 HERE Global B.V. and/or its affiliated companies. All rights reserved.
//
// This software, including documentation, is protected by copyright controlled by
// HERE Global B.V. All rights are reserved. Copying, including reproducing, storing,
// adapting or translating, any or all of this material requires the prior written
// consent of HERE Global B.V. This material also contains confidential information,
// which may not be disclosed to others without prior written consent of HERE Global B.V.
//
// Automatically generated. Do not modify. Your changes will be lost.
#include "cbridge/include/smoke/CalculatorListener.h"
#include "cbridge_internal/include/BaseHandleImpl.h"
#include "cbridge_internal/include/CachedProxyBase.h"
#include "smoke/CalculatorListener.h"
#include <memory>
#include <new>

void smoke_CalculatorListener_release(_baseRef handle) {
    delete get_pointer<std::shared_ptr<smoke::CalculatorListener>>(handle);
}
_baseRef smoke_CalculatorListener_copy(_baseRef handle) {
    return { new (std::nothrow)std::shared_ptr<smoke::CalculatorListener>(*get_pointer<std::shared_ptr<smoke::CalculatorListener>>(handle)) };
}
void smoke_CalculatorListener_onCalculationResult(_baseRef _instance, double calculationResult) {
    return get_pointer<std::shared_ptr<smoke::CalculatorListener>>(_instance)->get()->on_calculation_result(calculationResult);
}

class smoke_CalculatorListenerProxy : public std::shared_ptr<smoke::CalculatorListener>::element_type, public CachedProxyBase<smoke_CalculatorListenerProxy> {
public:
    using function_table_t = smoke_CalculatorListener_FunctionTable;
    smoke_CalculatorListenerProxy(smoke_CalculatorListener_FunctionTable&& functions)
     : mFunctions(std::move(functions))
    {
    }
    virtual ~smoke_CalculatorListenerProxy() {
        mFunctions.release(mFunctions.swift_pointer);
    }
    void on_calculation_result(double calculationResult) override {
        return mFunctions.smoke_CalculatorListener_onCalculationResult(mFunctions.swift_pointer, calculationResult);
    }
private:
    function_table_t mFunctions;
};

_baseRef smoke_CalculatorListener_createProxy(smoke_CalculatorListener_FunctionTable functionTable) {
    auto proxy = smoke_CalculatorListenerProxy::get_proxy(std::move(functionTable));
    if (proxy) {
        return { new (std::nothrow) std::shared_ptr<smoke::CalculatorListener>(std::move(proxy)) };
    } else {
        return { nullptr };
    }
}
