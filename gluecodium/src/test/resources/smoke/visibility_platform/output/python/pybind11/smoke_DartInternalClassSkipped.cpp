

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartInternalClassSkipped.h"

void register_DartInternalClassSkipped(py::module_& module) {
    py::class_<DartInternalClassSkipped>(module, "DartInternalClassSkipped")
        ;
}

