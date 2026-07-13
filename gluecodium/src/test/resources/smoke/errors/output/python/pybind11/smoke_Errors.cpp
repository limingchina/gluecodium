

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/Bar.h"
#include "smoke/Errors.h"
#include "smoke/Payload.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Errors = ::gluecodium::smoke::Errors;

void register_Errors(py::module_& module) {
    py::class_<Errors, std::shared_ptr<Errors>>(module, "Errors")
        .def("method_with_errors", &Errors::method_with_errors)
        .def("method_with_external_errors", &Errors::method_with_external_errors)
        .def("method_with_errors_and_return_value", &Errors::method_with_errors_and_return_value)
        .def("method_with_payload_error", &Errors::method_with_payload_error)
        .def("method_with_payload_error_and_return_value", &Errors::method_with_payload_error_and_return_value)
        ;
}

