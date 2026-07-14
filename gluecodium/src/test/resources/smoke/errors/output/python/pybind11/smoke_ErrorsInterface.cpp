

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

    void method_with_errors(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, ErrorsInterface, method_with_errors);
    }
    void method_with_external_errors(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, ErrorsInterface, method_with_external_errors);
    }
    ::std::string method_with_errors_and_return_value(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(::std::string, ErrorsInterface, method_with_errors_and_return_value);
    }
};

void register_ErrorsInterface(py::module_& module) {
    py::class_<ErrorsInterface, std::shared_ptr<ErrorsInterface>, ErrorsInterfaceTrampoline>(module, "ErrorsInterface")
        .def(py::init<>())
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

