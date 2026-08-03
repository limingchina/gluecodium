

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/Bar.h"
#include "smoke/Errors.h"
#include "smoke/Payload.h"
#include "string"

using Errors = ::smoke::Errors;
using InternalErrorCode = ::smoke::Errors::InternalErrorCode;



void register_smoke_Errors(py::module_& module) {
auto cls_Errors = py::class_<Errors, std::shared_ptr<Errors>>(module, "smoke_Errors")
        .def("__gluecodium_id__", [](const Errors& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("method_with_errors", &Errors::method_with_errors)
        .def_static("method_with_external_errors", &Errors::method_with_external_errors)
        .def_static("method_with_errors_and_return_value", &Errors::method_with_errors_and_return_value)
        .def_static("method_with_payload_error", &Errors::method_with_payload_error)
        .def_static("method_with_payload_error_and_return_value", &Errors::method_with_payload_error_and_return_value)
        ;

auto cls_ErrorsInternalErrorCode = py::enum_<InternalErrorCode>(cls_Errors, "InternalErrorCode")
        .value("ERROR_NONE", InternalErrorCode::ERROR_NONE)
        .value("ERROR_FATAL", InternalErrorCode::ERROR_FATAL)
        ;

auto cls_ErrorsExternalErrors = py::enum_<::fire::SomeEnum>(cls_Errors, "ExternalErrors")
        .value("NONE", ::fire::SomeEnum::NONE)
        .value("BOOM", ::fire::SomeEnum::BOOM)
        .value("BUST", ::fire::SomeEnum::BUST)
        ;

    static py::exception<::std::error_code> exc(cls_Errors, "InternalError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc.ptr());

    static py::exception<::std::error_code> exc(cls_Errors, "ExternalError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc.ptr());


}
