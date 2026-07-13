

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartInternalClassEnabled.h"

void register_DartInternalClassEnabled(py::module_& module) {
    py::class_<DartInternalClassEnabled>(module, "DartInternalClassEnabled")
        ;
}

