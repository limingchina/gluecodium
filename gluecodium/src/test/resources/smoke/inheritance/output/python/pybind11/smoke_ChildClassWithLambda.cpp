

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildClassWithLambda.h"

void register_ChildClassWithLambda(py::module_& module) {
    py::class_<ChildClassWithLambda>(module, "ChildClassWithLambda")
        ;
}

