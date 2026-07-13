

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Payload.h"
#include "smoke/WithPayload.h"

void register_WithPayloadError(py::module_& module) {
    py::exception<::std::error_code>(module, "WithPayloadError");
}

