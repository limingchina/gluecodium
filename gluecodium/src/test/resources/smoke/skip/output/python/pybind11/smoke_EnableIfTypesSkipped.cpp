

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnableIfTypesSkipped.h"

void register_EnableIfTypesSkipped(py::module_& module) {
    py::class_<EnableIfTypesSkipped>(module, "EnableIfTypesSkipped")
        ;
}

