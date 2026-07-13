

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartPublicClassSkipped.h"

void register_DartPublicClassSkipped(py::module_& module) {
    py::class_<DartPublicClassSkipped>(module, "DartPublicClassSkipped")
        ;
}

