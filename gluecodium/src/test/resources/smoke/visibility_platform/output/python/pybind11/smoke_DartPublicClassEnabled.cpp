

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartPublicClassEnabled.h"

void register_DartPublicClassEnabled(py::module_& module) {
    py::class_<DartPublicClassEnabled>(module, "DartPublicClassEnabled")
        ;
}

