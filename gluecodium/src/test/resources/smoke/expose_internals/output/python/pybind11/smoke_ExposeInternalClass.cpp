

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ExposeInternalClass.h"

void register_ExposeInternalClass(py::module_& module) {
    py::class_<ExposeInternalClass>(module, "ExposeInternalClass")
        ;
}

