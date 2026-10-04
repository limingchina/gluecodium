

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
#include "smoke/ErrorsInterface.h"
#include "smoke/Payload.h"
#include "string"

using ErrorsInterface = ::smoke::ErrorsInterface;
using InternalError = ::smoke::ErrorsInterface::InternalError;
using ExternalErrors = ::smoke::ErrorsInterface::ExternalErrors;

class ErrorsInterfaceTrampoline : public ErrorsInterface {
public:
    using ErrorsInterface::ErrorsInterface;
    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ErrorsInterface> m_impl;

    using method_with_errors_return_type = ::std::error_code;
    ::std::error_code method_with_errors(
            /* no args */ ) override {
        if (m_impl) {
            return m_impl->method_with_errors();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ErrorsInterface*>(this), "__gluecodium_callback_736d6f6b652e4572726f7273496e746572666163652e6d6574686f64576974684572726f7273")) {
            auto callback = py::get_override(static_cast<const ErrorsInterface*>(this), "__gluecodium_callback_736d6f6b652e4572726f7273496e746572666163652e6d6574686f64576974684572726f7273");
            auto result = callback();
            return result.is_none() ? std::error_code{} : result.cast<std::error_code>();
        }
        if (auto callback = py::get_override(static_cast<const ErrorsInterface*>(this), "method_with_errors")) {
            auto result = callback();
            return result.is_none() ? std::error_code{} : result.cast<std::error_code>();
        }
        py::pybind11_fail("Tried to call pure virtual function \"ErrorsInterface::method_with_errors\"");
    }
    using method_with_external_errors_return_type = ::std::error_code;
    ::std::error_code method_with_external_errors(
            /* no args */ ) override {
        if (m_impl) {
            return m_impl->method_with_external_errors();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ErrorsInterface*>(this), "__gluecodium_callback_736d6f6b652e4572726f7273496e746572666163652e6d6574686f645769746845787465726e616c4572726f7273")) {
            auto callback = py::get_override(static_cast<const ErrorsInterface*>(this), "__gluecodium_callback_736d6f6b652e4572726f7273496e746572666163652e6d6574686f645769746845787465726e616c4572726f7273");
            auto result = callback();
            return result.is_none() ? std::error_code{} : result.cast<std::error_code>();
        }
        if (auto callback = py::get_override(static_cast<const ErrorsInterface*>(this), "method_with_external_errors")) {
            auto result = callback();
            return result.is_none() ? std::error_code{} : result.cast<std::error_code>();
        }
        py::pybind11_fail("Tried to call pure virtual function \"ErrorsInterface::method_with_external_errors\"");
    }
    using method_with_errors_and_return_value_return_type = ::gluecodium::Return< ::std::string, ::std::error_code >;
    ::gluecodium::Return< ::std::string, ::std::error_code > method_with_errors_and_return_value(
            /* no args */ ) override {
        if (m_impl) {
            return m_impl->method_with_errors_and_return_value();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ErrorsInterface*>(this), "__gluecodium_callback_736d6f6b652e4572726f7273496e746572666163652e6d6574686f64576974684572726f7273416e6452657475726e56616c7565")) {
        PYBIND11_OVERRIDE_PURE_NAME(method_with_errors_and_return_value_return_type, ErrorsInterface, "__gluecodium_callback_736d6f6b652e4572726f7273496e746572666163652e6d6574686f64576974684572726f7273416e6452657475726e56616c7565", method_with_errors_and_return_value);
        }
        PYBIND11_OVERRIDE_PURE(method_with_errors_and_return_value_return_type, ErrorsInterface, method_with_errors_and_return_value);
    }
};



void register_smoke_ErrorsInterface(py::module_& module) {
auto cls_ErrorsInterface = py::class_<ErrorsInterface, std::shared_ptr<ErrorsInterface>, ErrorsInterfaceTrampoline>(module, "smoke_ErrorsInterface")
        .def("__gluecodium_id__", [](const ErrorsInterface& self) {
            return gluecodium::python::native_identity(self);
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ErrorsInterface> native) {
            auto self = std::make_shared<ErrorsInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("method_with_errors", [](ErrorsInterface& self) {
                const auto error = gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_errors(); });
                if (error) {
                    throw error;
                }
        })
        .def("method_with_external_errors", [](ErrorsInterface& self) {
                const auto error = gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_external_errors(); });
                if (error) {
                    throw error;
                }
        })
        .def("method_with_errors_and_return_value", [](ErrorsInterface& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_errors_and_return_value(); });
        })
        .def_static("method_with_payload_error", &ErrorsInterface::method_with_payload_error, py::call_guard<py::gil_scoped_release>())
        .def_static("method_with_payload_error_and_return_value", &ErrorsInterface::method_with_payload_error_and_return_value, py::call_guard<py::gil_scoped_release>())
        ;

auto cls_ErrorsInterfaceInternalError = py::enum_<InternalError>(cls_ErrorsInterface, "InternalError")
        .value("ERROR_NONE", InternalError::ERROR_NONE)
        .value("ERROR_FATAL", InternalError::ERROR_FATAL)
        ;

auto cls_ErrorsInterfaceExternalErrors = py::enum_<ExternalErrors>(cls_ErrorsInterface, "ExternalErrors")
        .value("NONE", ExternalErrors::NONE)
        .value("BOOM", ExternalErrors::BOOM)
        .value("BUST", ExternalErrors::BUST)
        ;

    static py::exception<::std::error_code> exc_InternalError(cls_ErrorsInterface, "InternalError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc_InternalError.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc_InternalError.ptr());

    static py::exception<::std::error_code> exc_ExternalError(cls_ErrorsInterface, "ExternalError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc_ExternalError.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc_ExternalError.ptr());


}
