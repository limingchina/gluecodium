

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/WithString.h"
#include "string"

void register_WithStringError(py::module_& module) {
    py::exception<::std::error_code>(module, "WithStringError");
}

