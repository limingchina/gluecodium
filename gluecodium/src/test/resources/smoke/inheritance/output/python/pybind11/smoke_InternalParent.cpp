

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InternalParent.h"

void register_InternalParent(py::module_& module) {
    py::class_<InternalParent>(module, "InternalParent")
        ;
}

