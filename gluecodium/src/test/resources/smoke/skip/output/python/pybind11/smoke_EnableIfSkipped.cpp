

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnableIfSkipped.h"

void register_EnableIfSkipped(py::module_& module) {
    py::class_<EnableIfSkipped>(module, "EnableIfSkipped")
        ;
}

