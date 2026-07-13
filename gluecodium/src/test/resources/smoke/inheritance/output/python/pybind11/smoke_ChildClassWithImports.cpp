

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildClassWithImports.h"

void register_ChildClassWithImports(py::module_& module) {
    py::class_<ChildClassWithImports>(module, "ChildClassWithImports")
        ;
}

