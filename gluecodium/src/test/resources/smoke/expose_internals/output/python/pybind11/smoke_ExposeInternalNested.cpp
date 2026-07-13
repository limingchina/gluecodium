

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ExposeInternalNested.h"

void register_ExposeInternalNested(py::module_& module) {
    py::class_<ExposeInternalNested>(module, "ExposeInternalNested")
        ;
}

