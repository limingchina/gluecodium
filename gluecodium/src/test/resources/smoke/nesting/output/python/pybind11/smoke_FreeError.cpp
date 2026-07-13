

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Free.h"
#include "smoke/FreeEnum.h"

void register_FreeError(py::module_& module) {
    py::exception<::std::error_code>(module, "FreeError");
}

