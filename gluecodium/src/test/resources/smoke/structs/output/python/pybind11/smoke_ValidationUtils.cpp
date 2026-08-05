

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ValidationUtils.h"

using ValidationUtils = ::smoke::ValidationUtils;
using ValidationErrorCode = ::smoke::ValidationUtils::ValidationErrorCode;



void register_smoke_ValidationUtils(py::module_& module) {
auto cls_ValidationUtils = py::class_<ValidationUtils>(module, "smoke_ValidationUtils")
        .def(py::init<>())
        ;

auto cls_ValidationUtilsValidationErrorCode = py::enum_<ValidationErrorCode>(cls_ValidationUtils, "ValidationErrorCode")
        .value("NONE", ValidationErrorCode::NONE)
        .value("VALIDATION_FAILED", ValidationErrorCode::VALIDATION_FAILED)
        ;

    static py::exception<::std::error_code> exc_ValidationError(cls_ValidationUtils, "ValidationError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc_ValidationError.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc_ValidationError.ptr());


}
