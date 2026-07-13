

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foo/Bar.h"
#include "smoke/Errors.h"
#include "smoke/Payload.h"
#include "smoke/WithPayload.h"
#include "string"

void register_Errors(py::module_& module) {
    py::class_<Errors>(module, "Errors")
        .def("method_with_errors", &Errors::method_with_errors)
        .def("method_with_external_errors", &Errors::method_with_external_errors)
        .def("method_with_errors_and_return_value", &Errors::method_with_errors_and_return_value)
        .def("method_with_payload_error", &Errors::method_with_payload_error)
        .def("method_with_payload_error_and_return_value", &Errors::method_with_payload_error_and_return_value)
        ;
}

