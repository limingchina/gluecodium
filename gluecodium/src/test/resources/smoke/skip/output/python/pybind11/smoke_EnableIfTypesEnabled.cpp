

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnableIfTypesEnabled.h"

void register_EnableIfTypesEnabled(py::module_& module) {
    py::class_<EnableIfTypesEnabled>(module, "EnableIfTypesEnabled")
        ;
}

