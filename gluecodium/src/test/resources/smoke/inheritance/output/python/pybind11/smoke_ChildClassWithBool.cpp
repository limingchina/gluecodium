

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildClassWithBool.h"

void register_ChildClassWithBool(py::module_& module) {
    py::class_<ChildClassWithBool>(module, "ChildClassWithBool")
        ;
}

