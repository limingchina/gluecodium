

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ErrorsInterface.h"
#include "smoke/Payload.h"
#include "smoke/WithPayload.h"
#include "string"

void register_ErrorsInterface(py::module_& module) {
    py::class_<ErrorsInterface, std::shared_ptr<ErrorsInterface>>(module, "ErrorsInterface")
        .def("method_with_errors", &ErrorsInterface::method_with_errors)
        .def("method_with_external_errors", &ErrorsInterface::method_with_external_errors)
        .def("method_with_errors_and_return_value", &ErrorsInterface::method_with_errors_and_return_value)
        .def("method_with_payload_error", &ErrorsInterface::method_with_payload_error)
        .def("method_with_payload_error_and_return_value", &ErrorsInterface::method_with_payload_error_and_return_value)
        ;
}

