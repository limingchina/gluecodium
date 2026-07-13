

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipMixed.h"

void register_SkipMixed(py::module_& module) {
    py::class_<SkipMixed>(module, "SkipMixed")
        ;
}

