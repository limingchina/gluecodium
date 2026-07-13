

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/AttributesCrash.h"
#include "string"

void register_AttributesCrashError(py::module_& module) {
    py::exception<::std::error_code>(module, "AttributesCrashError");
}

