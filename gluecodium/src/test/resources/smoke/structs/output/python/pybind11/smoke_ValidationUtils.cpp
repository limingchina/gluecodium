

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ValidationUtils.h"

void register_ValidationUtils(py::module_& module) {
    py::class_<ValidationUtils>(module, "ValidationUtils")
        ;
}

