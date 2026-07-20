

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ErrorsInterface.h"
#include "smoke/Payload.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ErrorsInterface = ::smoke::ErrorsInterface;

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
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_errors();
        }
        PYBIND11_OVERRIDE_PURE(method_with_errors_return_type, ErrorsInterface, method_with_errors);
    }
    using method_with_external_errors_return_type = ::std::error_code;
    ::std::error_code method_with_external_errors(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_external_errors();
        }
        PYBIND11_OVERRIDE_PURE(method_with_external_errors_return_type, ErrorsInterface, method_with_external_errors);
    }
    using method_with_errors_and_return_value_return_type = ::gluecodium::Return< ::std::string, ::std::error_code >;
    ::gluecodium::Return< ::std::string, ::std::error_code > method_with_errors_and_return_value(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_errors_and_return_value();
        }
        PYBIND11_OVERRIDE_PURE(method_with_errors_and_return_value_return_type, ErrorsInterface, method_with_errors_and_return_value);
    }
};

void register_ErrorsInterface(py::module_& module) {
    py::class_<ErrorsInterface, std::shared_ptr<ErrorsInterface>, ErrorsInterfaceTrampoline>(module, "ErrorsInterface")
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
            return self.method_with_errors();
        })

        .def("method_with_external_errors", [](ErrorsInterface& self) {
            return self.method_with_external_errors();
        })

        .def("method_with_errors_and_return_value", [](ErrorsInterface& self) {
            return self.method_with_errors_and_return_value();
        })

        .def_static("method_with_payload_error", &ErrorsInterface::method_with_payload_error)

        .def_static("method_with_payload_error_and_return_value", &ErrorsInterface::method_with_payload_error_and_return_value)

        ;
}

